#
# ed1c24

from ikcam.gfx import style

class Style (style.Style):
    """
    Automatiek style configuration file
    """
    title_y = 200
    subtitle1_y = 350
    subtitle2_y = 550
    button1_y = 850
    button2_y = 400
    button3_y = None

    ###SINGLE BUTTON CONFIGURATION
    button_width = 150 #doesnt matter, depends on the width of the text
    button_height = 50
    button_arc = 0
    button_color = (0.92,0.10,0.14,1) 
    button_color_secondary = (0.50, 0.50, 0.50, 1) #color of the buttons that are out of the normal flow
    button_color_pressed = (0, 0.35, 0.75, 1)
    button_font = "Ernest 32px"
    button_font_color = 'White'
    button_font_color_pressed = None
    button_border_color = (0.85,0.85,0.85,1) #tuple with 4 numbers between 0 and 1.0
    button_border_color_pressed = (0, 0.35, 0.75, 1)
    button_border_width = 0
    spaceBetweenButtons = 100

    ###TEXTBOX CONFIGURATION
    textbox_width = 1500
    textbox_font = 'Ernest 50px'
    textbox_font_color = "#ed1c24"

    textbox_text_separation = 5  #separation between the box and the text, lef allignement
    textbox_title_font = 'Ernest 50px'
    textbox_title_font_color = "#ed1c24"
    textbox_title_vertical_separation = 10
    textbox_border_color = "#777777"
    textbox_border_width = 3


    ##title setup
    title_font = "Ernest 50px"  
    title_font_color = "#ed1c24"  #red color  

    ##subtitle1 setup
    subtitle1_font = "Ernest 64px"
    subtitle1_font_color = "#ed1c24"

    ##subtitle2 setup
    subtitle2_font = "Ernest 36px"
    subtitle2_font_color = "Black"
    
    ##subtitle3 setup
    subtitle3_font = "Ernest 28px"
    subtitle3_font_color = "Black"

    #coinbox setup
    coinbox_font = "Ernest 100px"
    coinbox_horizontal_separation=30

    shadowedtext_font="Ernest %dpx"

    countdown_font = "Floraless"
    countdown_font_color = "#d2232a"
    countdown_font_size = 240

    stepprogress_font = "Floraless"
    stepprogress_color = "#d2232a"
    stepprogress_highlight_color = "#FFFF00"

    ###IMAGE SETUP (size of pngs shown):
    arrow_height = 300
    arrow_down_height = 300
    cardPicture_height = 340
    coinsPicture_height = 340

    tag_icon_height = 100
    tag_icon_x = 500
    tag_icon_y = 500
    placeTagPicture_height = 300

    spaceBetweenKeywordImages = 100
    skipbutton_height = 40

    ikcamtext_font="Ernest"
    ikcamtext_font_size = 80
