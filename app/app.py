# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from modules.nst import apply_neural_style_transfer

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


img_box_width = '400px'
img_box_margin = '10px'


def create_image_box(id_box, path_default_img='assets/images/brad_pitt.jpg', button1_txt = 'Select an Image', elmt2_type='upload', elmt2_msg=html.Div(['Drag and Drop or ', html.A('Select Files')])):
    
    elmt_list = list()

    ## add image
    elmt_img =  html.Img(id=id_box+'-img', src=path_default_img,
                 style={
                     'display':'block',
                     'borderWidth':'1px',
                     'width':img_box_width,
                     'height':img_box_width,
                     'margin':img_box_margin
                     }
                 )
    elmt_list.append(elmt_img)

    ## add button 1
    elmt_button = html.Button(button1_txt, id=id_box+'-button-1', n_clicks=0,
                    style={
                        'display':'block',
                        'width':img_box_width,
                        'margin':img_box_margin
                    })

    elmt_list.append(elmt_button)

    ## add button 2 or upload
    if elmt2_type == "upload":
         elmt_upload = dcc.Upload(
                  id=id_box+'-upload',
                  children=elmt2_msg,
                  style={
                         'display':'block',
                         'borderWidth':'1px',
                         'width':img_box_width,
                         'height':'30px',
                         'borderStyle':'dashed',
                         'borderWidth':'1px',
                         'textAlign':'center',
                         'margin':img_box_margin
                      
                  },
                  multiple=False #Allow multiple files to be uploaded
             )
         elmt_list.append(elmt_upload)
    elif elmt2_type == 'button':
        elmt_button2 = html.Button(elmt2_msg, id=id_box+'-button-2', n_clicks=0,
                        style={
                            'display':'block',
                            'width':img_box_width,
                            'margin':img_box_margin
                        })
        elmt_list.append(elmt_button2)
    #elmt_list.append(elmt_upload)
    img_box = html.Div(children=elmt_list, style={'margin': '20px'})
    return img_box


img_box1 = create_image_box('box-1', button1_txt = 'Select a Content Image', path_default_img='assets/images/brad_pitt.jpg')
img_box2 = create_image_box('box-2', button1_txt = 'Select a Style Image', path_default_img='assets/images/mosaic.jpg')
img_box3 = create_image_box('box-3', button1_txt = 'Get Result Image', path_default_img='assets/images/gray.jpeg', elmt2_type='button', elmt2_msg='Download Image !')

app.layout = html.Div(children=[
    html.H1(children='Pictulize'),
    html.H2(children='Create your art image !'),
    
    html.Div(children=[
        img_box1,
        img_box2,
        img_box3
        ], style={'display':'flex', 'margin-left':'200px'})
])

class ButtonCallback():
    def __init__(self):
        self.n_clicks = {'box-1-button-1':0, 'box-2-button-1':0, 'box-3-button-1':0}

    def update_n_clicks(self, nclicks, bt_name):
        self.n_clicks[bt_name] = nclicks

button_callback = ButtonCallback()

@app.callback(
        Output(component_id="box-3-img", component_property="src"),
        [Input(component_id='box-3-button-1', component_property='n_clicks')],
        [State(component_id="box-1-img", component_property="src"),
         State(component_id="box-2-img", component_property="src")]
        )
def update_img_3(b3_b1_nclick, path_img_content, path_img_style):
    
    b3_b1_nclick = 0 if b3_b1_nclick is None else b3_b1_nclick

    if b3_b1_nclick != button_callback.n_clicks['box-3-button-1']:
        button_callback.update_n_clicks(b3_b1_nclick, 'box-3-button-1')
        return apply_neural_style_transfer(path_img_content, path_img_style, path_img_output='assets/images/output.jpg')
    else:
        return 'assets/images/gray.jpeg'


if __name__ == '__main__':
    app.run_server(debug=True, port=8086)
    #app.run_server(debug=False, port=8086)
