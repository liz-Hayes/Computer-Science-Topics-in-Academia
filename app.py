from dash import Dash, html, dcc, callback, Output, Input, State, ALL, ctx, MATCH
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import mysql_utils
import mongodb_utils
import neo4j_utils
import random
from dash import html

# Initialize
app = Dash(__name__)

#Get list of all keywords
q_SQL = "SELECT keyword.name, keyword.id FROM keyword"
keywords= mysql_utils.query(q_SQL)
keywords_dict = keywords.set_index('id')['name'].to_dict()


#Make card with university information
def make_uni_card(input_list):
    [id, uni_name, krc, uni_url] = input_list
    card = dbc.Card(
            [dbc.Row([
                    dbc.Col(  
                        dbc.CardImg(src=uni_url, top=True,style={ "height": "5rem" ,"max-width": "5rem","object-fit": "contain","vertical-align": "middle"},),className ="col-md-4"
                    ),
                    dbc.Col(
                        dbc.CardBody(
                        [
                            html.H6(uni_name, className="card-title", id="prof_name", style={"font-size":"12px"}),
                            dbc.Button("See faculty", color="primary", id={"type": "see_fac_button", "index":str(id)},  style={"font-size":"12px"})
                        ]
                        ),
                    )
                ],align="center")
    
            ],
            style={"text-align": "center"}
        )
    return card
#make card for posted comments
def make_comment_card(input_list):
    [id, text, num_likes,keyword_id] = input_list
    card = dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.P(text,className="card-text",style={"margin":0,"font-size":"12px"}),
                        dbc.Row([
                        dbc.Col(dbc.Button("♥", color="info", id={"type": "like_button", "index":id}, style={"font-size":"12px"})),
                        dbc.Col(html.P(str(num_likes)+" likes",className="card-text",style={"margin":0,"font-size":"12px"}, id={"type": "likes", "index":id})),
                        ], align="center")
                    ]
                ),
            ],
            style={"text-align": "center"}
        )
    return card

#make carousel of top faculty images and info
def make_carousel(input_df):
    car_items = []
    for index, row in input_df.iterrows():
        [fac_name, fac_url, krc, uni, email, phone] = row
        if email == "" and phone =="":
            caption =""
        elif email == "":
            caption = phone
        elif phone == "":
            caption = email
        else:
            caption = email + "/" + phone 
        item = {"key":index, "src":fac_url, "header":fac_name, "caption":caption, "caption_class_name":"mark","img_style":{"height": "28rem", "object-fit": "contain", "margin":0,"background-color":"LightBlue"},} 
        car_items.append(item)
    carousel= dbc.Carousel(items=car_items,controls=True, indicators=False, variant="dark")
    return carousel


#App Layout

row1 = dbc.Row([dbc.Col(html.H5("Top Universities", id="top_uni_id",style={'textAlign': 'center'})),dbc.Col(html.H5("Top Faculty", id="top_fac_caption",style={'textAlign': 'center'}))],align="center", style = {"margin-top": "20px"})
card_stack = dbc.Stack([dbc.Card(id="uni_card_1"), dbc.Card(id="uni_card_2"),dbc.Card(id="uni_card_3"),dbc.Card(id="uni_card_4"),dbc.Card(id="uni_card_5")])
row2 = dbc.Row([dbc.Col(card_stack), dbc.Col( html.Div(id="carousel"))],align="center", style = {"margin-top": "20px"})
row3 = dbc.Row([dbc.Col(html.H5(children="Top 5 Most Relevant Publications to Keyword", id="top_pub_title"), style={'textAlign': 'center'}), dbc.Col(html.H5("Publications over Time",id="keyword_pop_graph_title"), style={'textAlign': 'center'})],align="center", style = {"margin-top": "20px"})
row4 = dbc.Row([dbc.Col(html.Div(id='relevant_pubs_table')), dbc.Col(dcc.Graph( id="keyword_pop_graph"))],align="center", style = {"margin-top": "20px"})
right_stack = dbc.Stack([dcc.Input(id='comment', value='Comment...', type = 'text'),html.Button(id='submit-button', type='submit', children="Submit"),html.Div(id='comments_container_div', children=[], style={"maxHeight": "50rem", "overflow": "scroll"})])
left_stack = dbc.Stack([row1,row2,row3,row4])

app.layout =dbc.Container(
    [
    dbc.Row([
        dbc.Col(html.H5("Choose a keyword to explore", style={"color":"white",'textAlign': 'center'}), width =4), 
        dbc.Col(dcc.Dropdown(keywords_dict, 0, id='keyword-dropdown'), width=8)
        ], style={"background-color": "#772953","margin-top": "20px", "height": "3rem" },),
    dbc.Row([dbc.Col(left_stack),dbc.Col(right_stack, width=2)],)
])


#Callbacks

@callback(Output('comments_container_div', 'children'),
          Output('comment', 'value'),
          Input('keyword-dropdown', 'value'),
          Input('submit-button', 'n_clicks'),
          State('comment', 'value'),
          )
def display_comments_for_keyword(selected_keyword_id, clicks, comment_value):
        triggered_id = ctx.triggered_id
        query_result = mysql_utils.query("SELECT id FROM keyword WHERE id = '" + str(selected_keyword_id)+"';")
        if triggered_id == 'submit-button':
            id = random.randint(0,2147483647)
            i1 = ("INSERT INTO comments"
               "(id, text, num_likes, keyword_id)"
               "VALUES (%s, %s,%s,%s)")
            i2 = (id, comment_value, 0, int(selected_keyword_id))
            mysql_utils.insert(i1,i2)

        query_result = mysql_utils.query("SELECT *FROM comments WHERE  keyword_id =" + str(selected_keyword_id)+";")
        cards = []
        for index, row in query_result.iterrows():
            cards.append(make_comment_card(row))
        return cards, ""


@callback(
        Output({"type": "likes", "index": MATCH}, 'children'),
        Input({"type": "like_button", "index": MATCH}, "n_clicks"),
        State({"type": "like_button", "index": MATCH}, "id"),
        prevent_initial_call=True
        )
def update_comments(n_clicks,id):
    if n_clicks is not None:
        comment_id = id['index']
        update_stmt = "UPDATE comments SET num_likes= num_likes +1 WHERE id = " + str(comment_id)
        mysql_utils.exec(update_stmt)
        query = "SELECT num_likes FROM comments WHERE  id = " + str(comment_id)
        q_result = mysql_utils.query(query)
        num_likes = q_result['num_likes'].values[0]
        return str(num_likes) + " likes"

@callback(
    Output(component_id='keyword_pop_graph', component_property='figure'),
    Output(component_id='keyword_pop_graph_title', component_property='children'),
    Input('keyword-dropdown', 'value')
    )
def update_keyword_pop_graph(selected_keyword_id):
    selected_keyword_name = keywords_dict[int(selected_keyword_id)]
    query1 = "SELECT year, COUNT(DISTINCT publication.id) AS 'Number of Publications' FROM publication, publication_keyword, keyword WHERE publication.id = publication_keyword.publication_id AND publication_keyword.keyword_id=keyword.id and keyword.id = '"+str(selected_keyword_id)+"' GROUP BY year;"
    query_result = mysql_utils.query(query1)
    fig = px.line( query_result, x = "year", y='Number of Publications', labels={
                     "Number of Publications'": "Number of Publications Containing the keyword'" +selected_keyword_name+"'",
                 },)
    title ="Popularity of Keyword '" + selected_keyword_name + "' Over Time",                  
    return fig, title


@callback(
    Output('uni_card_1', 'children'),
    Output('uni_card_2', 'children'),
    Output('uni_card_3', 'children'),
    Output('uni_card_4', 'children'),
    Output('uni_card_5', 'children'),
    Output('top_uni_id', 'children'),
    Input('keyword-dropdown', 'value')
    )
def update_uni_cards(selected_keyword_id):
    selected_keyword_name = keywords_dict[int(selected_keyword_id)]

    q = "SELECT university.id, university.name AS University, SUM(KRC) AS 'Relevancy Score', university.photo_url AS photo_url FROM university, (SELECT faculty.id, faculty.university_id,SUM(publication_keyword.score * publication.num_citations)AS KRC FROM faculty,faculty_publication,keyword, publication, publication_keyword WHERE faculty.id = faculty_publication.faculty_id AND faculty_publication.publication_id=publication.id AND publication_keyword.publication_id = publication.id AND publication_keyword.keyword_id = keyword.id AND keyword.id = \'"+str(selected_keyword_id)+"\' GROUP BY faculty.id) AS fac_krc WHERE university.id = fac_krc.university_id GROUP BY university.id ORDER BY SUM(KRC) DESC LIMIT 10;"
    query_result = mysql_utils.query(q)
    top_uni_heading ="Top Universities for "+ selected_keyword_name.title()
    return  make_uni_card(query_result.iloc[0]), make_uni_card(query_result.iloc[1]),make_uni_card(query_result.iloc[2]),make_uni_card(query_result.iloc[3]),make_uni_card(query_result.iloc[4]),top_uni_heading



@callback(
    Output('carousel', 'children'),
    Output('top_fac_caption', 'children'),
    Input('keyword-dropdown', 'value'),
    Input({"type" :"see_fac_button", "index":ALL}, "n_clicks")
    )
def update_faculty_carousel(selected_keyword_id, clicks):
    triggered_id = ctx.triggered_id
    caption = "a caption"
    selected_keyword_name = keywords_dict[int(selected_keyword_id)]
    if triggered_id == "keyword-dropdown"  or triggered_id is None:
        q_neo4j="MATCH (f:FACULTY)-[publish:PUBLISH]->(publication:PUBLICATION)-[l:LABEL_BY]->(k:KEYWORD {id:'k"+str(selected_keyword_id)+"'}),(f)-[:AFFILIATION_WITH]->(i:INSTITUTE) WITH f.name AS name, f.photoUrl AS photoUrl, l.score AS score, publication.numCitations AS numCitations, i.name AS uni, f.email as email, f.phone as phone RETURN name, photoUrl, SUM(score*numCitations) as KRC, uni, email, phone ORDER BY KRC DESC LIMIT 5"
        caption = "Top Faculty for "+ selected_keyword_name.title()
    else:
        if clicks is not None:
            uni_id = "i"+triggered_id['index']
            query_result_neo4j = neo4j_utils.query("MATCH (i:INSTITUTE {id:'"+uni_id+"'}) WITH i.name as name RETURN name")
            uni_name =query_result_neo4j[0].values[0]
            q_neo4j="MATCH (f:FACULTY)-[publish:PUBLISH]->(publication:PUBLICATION)-[l:LABEL_BY]->(k:KEYWORD {id:'k"+str(selected_keyword_id)+"'}),(f)-[:AFFILIATION_WITH]->(i:INSTITUTE {id: '"+uni_id+"'}) WITH f.name AS name, f.photoUrl AS photoUrl, l.score AS score, publication.numCitations AS numCitations, i.name AS uni, f.email as email, f.phone as phone RETURN name, photoUrl, SUM(score*numCitations) as KRC, uni, email, phone ORDER BY KRC DESC LIMIT 5"
            caption = "Top Faculty at " +uni_name.title() +" for " + selected_keyword_name.title()
    query_result_neo4j = neo4j_utils.query(q_neo4j)
    query_result_neo4j = query_result_neo4j.fillna('')
    return make_carousel(query_result_neo4j), caption

@callback(
    Output('relevant_pubs_table','children'),
    Output(component_id='top_pub_title', component_property='children'),
    Input('keyword-dropdown', 'value')
    )
def update_relevant_pubs_table(selected_keyword_id):
    selected_keyword_name = keywords_dict[int(selected_keyword_id)]
    query_result = mongodb_utils.query("publications",[{'$unwind': '$keywords'}, {'$match':{'keywords.id':int(selected_keyword_id)}}, {'$project':{"_id":0, 'Title':"$title", "score":"$keywords.score", 'Venue':'$venue', 'Year':"$year", 'Number of Citations':"$numCitations"}}, {'$sort': {'score': -1}}, {'$limit':5}, {'$project':{'score':0}}])
    title = "Top 5 Most Relevant Publications to " + selected_keyword_name.title()
    return dbc.Table.from_dataframe(query_result, striped=True, bordered=True, hover=True,style= {"font-size":"12px", "text-align": "center"}), title



if __name__ == '__main__':
    app.run(debug=True)

