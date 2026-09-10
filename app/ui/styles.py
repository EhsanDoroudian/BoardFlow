DARK_THEME = """
QMainWindow {
    background-color: #12101A;
}

QWidget {
    color: #F2F0F7;
    font-family: "Ubuntu";
    font-size: 14px;
}

QLabel#title {
    color: #B56CFF;
    font-size: 28px;
    font-weight: bold;
}

QLabel#history_title {
    color: #FFFFFF;
    font-size: 18px;
    font-weight: bold;
}

QLineEdit {
    background-color: #1D1928;
    border: 1px solid #342B45;
    border-radius: 10px;
    padding: 10px;
    color: #FFFFFF;
}

QLineEdit:focus {
    border: 1px solid #9B5CFF;
}

QListWidget {

    background-color: #1D1928;

    border: 1px solid #342B45;

    border-radius: 10px;

    color: #F2F0F7;

    padding: 6px;

}

QListWidget::item {

    padding: 10px;

    border-radius: 8px;

}

QListWidget::item:selected {

    background-color: #34204F;

}
"""


LIGHT_THEME = """
QMainWindow {
    background-color: #F5F3F8;
}

QWidget {
    color: #211B2B;
    font-family: "Ubuntu";
    font-size: 14px;
}

QLabel#title {
    color: #7138C8;
    font-size: 28px;
    font-weight: bold;
}

QLabel#history_title {
    color: #211B2B;
    font-size: 18px;
    font-weight: bold;
}

QLineEdit {
    background-color: #FFFFFF;
    border: 1px solid #D5CEE0;
    border-radius: 10px;
    padding: 10px;
    color: #211B2B;
}

QLineEdit:focus {
    border: 1px solid #7138C8;
}

QListWidget {

    background-color: #FFFFFF;

    border: 1px solid #D5CEE0;

    border-radius: 10px;

    color: #211B2B;

    padding: 6px;

}

QListWidget::item {

    padding: 10px;

    border-radius: 8px;

}

QListWidget::item:selected {

    background-color: #E8DDF5;

}
"""