down_arrow = '''

    QComboBox::drop-down{
        border: 0px;
    }
    QComboBox::down-arrow{
        image: url(icons/down-arrow.png);
        width: 12px;
        height: 12px;
        right:7px;
    }
    QComboBox::down-arrow:hover{
        width: 17px;
        height: 17px;
    }
    QListView{
        background-image: url(interface//background.png);
        color: white;
        }
    QListView::item:selected:hover{
        background-color: #2e2e2e;
        color: #2e2e2e;
        }

'''

buttons = '''

    QPushButton
    {
    font-family:corbel;
    font-size:24px;
    color:white;
    background-color: rgba(19,18,18, 80);
    border-color: #4A4949;
    border-radius:15px;
    border-style:outset;
    border-width:1px;
    border-color:white;
    }

    QPushButton:disabled
    {
    background-color: rgba(100,18,18, 100);
    border-width: 1px;
    border-color: #3A3939;
    border-style: solid;
    padding-top: 5px;
    padding-bottom: 5px;
    padding-left: 10px;
    padding-right: 10px;
    border-radius: 2px;
    color: #454545;
    }

    QPushButton:hover {
    border-width: 1px;
    border-color: #3d8ec9;
    border-style: solid;
    }

'''

Qmenu = '''

    QMenuBar
    {
        font-size:18px;
        background-color: #262626;
        color: #e0e0e0;
    }
    QMenuBar::item
    {
        background-color: transparent;
    }
    QMenuBar::item:selected
    {
        background-color: #ffffff;
        color: #2e2e2e;
    }
    QMenu
    {
        font-size:18px;
        background-color: #262626;
        color: #ffffff;
    }
    QMenu::item:selected
    {
        background-color: #ffffff;
        color: #2e2e2e;
    }

'''