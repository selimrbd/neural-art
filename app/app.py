# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from modules.nst import apply_neural_style_transfer
from pathlib import Path
import base64
from flask import send_from_directory
import time

APP_NAME = 'Neural Art'

ROOT_PATH = Path(__file__).parent

IMG_USER_DIRECTORY = ROOT_PATH/'assets/images/user'

IMG_CONTENT_DIRECTORY = ROOT_PATH/'assets/images/content'
IMG_STYLE_DIRECTORY = ROOT_PATH/'assets/images/style'
IMG_OTHER_DIRECTORY = ROOT_PATH/'assets/images/other'
if not IMG_USER_DIRECTORY.exists():
    IMG_USER_DIRECTORY.mkdir()

IMG_BOX_WIDTH = '400px'
IMG_BOX_HEIGHT = '400px'
IMG_BOX_MARGIN = '10px'
COLOR_BUTTON_DISABLED = 'rgba(191, 191, 191, 1)'
COLOR_BUTTON_ENABLED = 'rgba(41, 241, 195, 1)'

PATH_LOADING_ANIMATION = IMG_OTHER_DIRECTORY/'rainbow.gif'
PATH_DEFAULT_CONTENT = IMG_CONTENT_DIRECTORY/'brad_pitt.jpg'
PATH_DEFAULT_STYLE = IMG_STYLE_DIRECTORY/'mosaic.jpg'
PATH_DEFAULT_NOPICTURE = IMG_OTHER_DIRECTORY/'no_picture.jpg'

DOWNLOAD_BUTTON_TEXT = 'Download'
RUN_NST_BUTTON_TEXT = 'Combine the images !'
PROCESSING_BUTTON_TEXT = 'Processing...'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = APP_NAME

## create the element containing the (image + image selection / upload / download)
def create_image_group(id_box, path_default_img, button1_txt='Select an Image', elmt2_type='upload', elmt2_msg=html.Div(['Drag and Drop or ', html.A('Select Files')])):
    
    elmt_list = list()
    ## add image
    id_img = f'{id_box}-img'
    elmt_img =  html.Div(id=f'container-{id_img}', children=[html.Img(id=id_img, src=str(path_default_img),
                 style={
                     'display':'block',
                     'width':IMG_BOX_WIDTH,
                     'height':IMG_BOX_HEIGHT,
                     'margin':IMG_BOX_MARGIN
                     }
                 )])
    elmt_list.append(elmt_img)

    ## add button 1
    id_button1 = f'{id_box}-button-1'
    elmt_button = html.Div(id=f'container-{id_button1}', children=[html.Button(button1_txt, id=id_button1, n_clicks=0,
                    style={
                        'display':'block',
                        'width':IMG_BOX_WIDTH,
                        'margin':IMG_BOX_MARGIN
                    })])
    elmt_list.append(elmt_button)

    ## add button 2 or upload
    id_button2 = f'{id_box}-upload'
    if elmt2_type == "upload":
         elmt_upload = dcc.Upload(
                  id=id_button2,
                  children=elmt2_msg,
                  style={
                         'display':'block',
                         'borderWidth':'1px',
                         'width':IMG_BOX_WIDTH,
                         'height':'30px',
                         'borderStyle':'dashed',
                         'borderWidth':'1px',
                         'textAlign':'center',
                         'margin':IMG_BOX_MARGIN
                      
                  },
                  multiple=False #Allow multiple files to be uploaded
             )
         elmt_list.append(elmt_upload)
    elif elmt2_type == 'download-button':
        elmt_download_button = html.Div(id=id_box+'-download-button-container',
                                children=[html.Form(id=f'{id_box}-download-form', children=[html.Button(elmt2_msg, id=f'{id_box}-download-button',
                                                                                            style={
                                                                                                'display':'block',
                                                                                                'width':IMG_BOX_WIDTH,
                                                                                                'margin':IMG_BOX_MARGIN
                                                                                            })],
                                                    action='')],
                                style={'margin':'0px', 'padding':'0px'})
        elmt_list.append(elmt_download_button)
    
    img_box = html.Div(children=elmt_list, style={'margin': '20px'})
    return img_box


img_box1 = create_image_group('box-1', button1_txt='Select from Gallery', path_default_img=PATH_DEFAULT_CONTENT)
img_box2 = create_image_group('box-2', button1_txt='Select from Gallery', path_default_img=PATH_DEFAULT_STYLE)
img_box3 = create_image_group('box-3', button1_txt='Get Result Image', path_default_img=PATH_DEFAULT_NOPICTURE, elmt2_type='download-button', elmt2_msg=DOWNLOAD_BUTTON_TEXT)

app.layout = html.Div(children=[
    html.H1(children=APP_NAME),
    html.Div(id='what-is-this', children=[
    html.H3(children='What is this ?'),
    dcc.Markdown('A **free service** to create artistic images in 1 click, by mixing one picture **content** with the **style** of another')
    ]),
    
    html.H3(children='Create your art image !'),
    html.Div(id='create-art', children=[
        img_box1,
        img_box2,
        img_box3
        ], style={'display':'flex', 'margin-left':'200px'}),
    html.Div(id='void'),
    html.Div(id='nst-trigger', style=dict(display='none'))
])


## handle user picture upload
def save_file(name, content, save_dir):
    """Decode and store a file uploaded with Plotly Dash."""
    save_dir = Path(save_dir)
    data = content.encode("utf8").split(b";base64,")[1]
    path_file = str(save_dir/name)
    with open(save_dir/name, "wb") as fp:
        fp.write(base64.decodebytes(data))
    return path_file


def create_callback_img_upload(id_img, id_upload, path_default_img, path_save_dir):
    @app.callback(
        Output(id_img, 'src'),
        [Input(id_upload, 'filename'), Input(id_upload, 'contents')]
        )
    def upload_user_img(filenames, contents):
         if filenames is not None and contents is not None:
             filenames = [filenames] if type(filenames) is str else filenames
             contents = [contents] if type(contents) is str else filenames
             for (f,c) in zip(filenames, contents):
                 path_file = save_file(f,c, path_save_dir)
         else:
             path_file = str(path_default_img)
         return path_file
    return upload_user_img

upload_user_content_img = create_callback_img_upload(id_img='box-1-img', id_upload='box-1-upload', path_default_img=IMG_CONTENT_DIRECTORY/'brad_pitt.jpg', path_save_dir=IMG_USER_DIRECTORY)
upload_user_style_img = create_callback_img_upload(id_img='box-2-img', id_upload='box-2-upload', path_default_img=IMG_STYLE_DIRECTORY/'mosaic.jpg', path_save_dir=IMG_USER_DIRECTORY)

## NEURAL STYLE TRANSFER COMPUTATION
class ButtonCallback():
    def __init__(self):
        self.n_clicks = {'box-1-button-1':0, 'box-2-button-1':0, 'box-3-button-1':0}
    def update_n_clicks(self, nclicks, bt_name):
        self.n_clicks[bt_name] = nclicks

button_callback = ButtonCallback()

## display loading image
@app.callback(
        [Output(component_id="box-3-img", component_property="src"), Output('box-3-button-1', 'disabled'), Output('box-3-button-1', 'style'),Output('box-3-button-1', 'children'), Output('nst-trigger', 'children')],
        [Input(component_id='box-3-button-1', component_property='n_clicks')]
        )
def display_loading(b3_b1_nclick):
    
    list_outputs = list()
    b3_b1_nclick = 0 if b3_b1_nclick is None else b3_b1_nclick

    if b3_b1_nclick > 0:
    #if b3_b1_nclick != button_callback.n_clicks['box-3-button-1']:
        button_callback.update_n_clicks(b3_b1_nclick, 'box-3-button-1')
        list_outputs = [str(PATH_LOADING_ANIMATION), True, dict(display='block', width=IMG_BOX_WIDTH, margin=IMG_BOX_MARGIN, backgroundColor=COLOR_BUTTON_DISABLED), PROCESSING_BUTTON_TEXT, 1]
    else:
        list_outputs = [str(PATH_DEFAULT_NOPICTURE), True, dict(display='block', width=IMG_BOX_WIDTH, margin=IMG_BOX_MARGIN, backgroundColor=COLOR_BUTTON_ENABLED), RUN_NST_BUTTON_TEXT, 0]
    return list_outputs


## run neural style transfer
@app.callback(
        [Output("container-box-3-img","children"), Output('container-box-3-button-1', 'children')],
        [Input(component_id='nst-trigger', component_property='children')],
        [State(component_id="box-1-img", component_property="src"),
         State(component_id="box-2-img", component_property="src")]
        )
def run_nst(value, path_img_content, path_img_style):

    list_outputs = list()
    new_button = html.Button(RUN_NST_BUTTON_TEXT, id='box-3-button-1', disabled=False, style=dict(display='block', width=IMG_BOX_WIDTH, margin=IMG_BOX_MARGIN, backgroundColor=COLOR_BUTTON_ENABLED))
    if value == 1:
        path_img_output = str(Path(IMG_USER_DIRECTORY)/f'output-{time.time()}.jpg') ## add a timestamp to avoid caching problems when name doesn't change
        path_img_output = apply_neural_style_transfer(path_img_content, path_img_style, path_img_output=path_img_output)
        new_img = html.Img(id='box-3-img', src=str(path_img_output), style=dict(display='block', width=IMG_BOX_WIDTH, height=IMG_BOX_HEIGHT, margin=IMG_BOX_MARGIN))
        list_outputs = [new_img, new_button]
    else:
        new_img = html.Img(id='box-3-img', src=str(PATH_DEFAULT_NOPICTURE), style=dict(display='block', width=IMG_BOX_WIDTH, height=IMG_BOX_HEIGHT, margin=IMG_BOX_MARGIN))
        list_outputs = [new_img, new_button]
    return list_outputs

## download file
@app.server.route('/download_image/<string:img_name>')
def download_file(img_name):
    print(f'user downloaded image: {img_name}')
    return send_from_directory(str(IMG_USER_DIRECTORY), img_name, as_attachment=True)

@app.callback(
        Output('box-3-download-form', 'action'),
        [Input('box-3-img', 'src')]
        )
def update_download_button(path_img):
    img_name = Path(path_img).name
    return f'/download_image/{img_name}'

if __name__ == '__main__':
    #app.run_server(debug=True, port=5000)
    app.run_server(debug=False, host='0.0.0.0', port=5000)
