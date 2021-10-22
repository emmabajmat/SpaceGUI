import io
import sys
import folium
from fetch import DataFetcher

from PyQt5 import (
    QtWebEngineWidgets,
    QtWidgets,
    QtCore,
    QtGui
)

from PyQt5.QtWidgets import (
    QHBoxLayout,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QLabel
)


class ApplicationWindow(QtWidgets.QMainWindow):
    """The main class which makes the application window.

    Args:
        QtWidgets ([QMainWindow]): Inherits from QtWidgets.QMainWindow to
        create a child class.
    """

    def __init__(self):
        """Initialize the ApplicationWindow Class."""
        super().__init__()
        self.initWindow()

    def initWindow(self):
        """Initialize window with settings."""
        self.setWindowTitle('Upcoming Launches')
        self.setFixedWidth(640)
        self.setFixedHeight(400)
        self.tabUI()

    def tabUI(self):
        """Create the table style UI."""
        self.table_widget = TabWidget(self, dataFetcher=DataFetcher())
        self.setCentralWidget(self.table_widget)


class TabWidget(QWidget):
    """Extension of the QWidget class to make a custom style tabular widget style.

    Args:
        QWidget ([QWidget]): Inherits from QWidget to create a child class.
    """

    def __init__(self, parent, dataFetcher):
        """Initialize the TabWidget Class.

        Args:
            parent ([ApplicationWindow]): Window to which this widget is
            attached.
            dataFetcher ([DataFetcher]): The class responsible for passing
            data.
        """
        super(QWidget, self).__init__(parent)
        self.data = dataFetcher
        self.layout = QVBoxLayout(self)
        self.initUI()

    def initUI(self):
        """Initialize UI, makes a TabPage for every result
        we get from the API"""
        self.tabs = QTabWidget()
        self.tabs.resize(300, 200)

        for index in range(0, 10):
            self.tabs.addTab(self.tabPageUI(index), f"{index+1}")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def tabPageUI(self, idx):
        """Create the default UI for a tab page.
        Other functions are called to keep the code clear.

        Args:
            idx ([int]): Index of entry in the results array.

        Returns:
            [QWidget]: The complete tabpage widget in which the
            layout is defined.
        """
        TabPage = QWidget()

        # Vertical layout containing the name of the launch service provider
        vertical_layout = QVBoxLayout()
        vertical_layout.addLayout(self.top_layout(idx))

        # Horizontal layout containing two vertical layouts,
        # one for the map, one for the mission info.
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addLayout(self.left_layout(idx), 1)
        horizontal_layout.addLayout(self.right_layout(idx), 1)

        # Merge everything in one single layout
        vertical_layout.addLayout(horizontal_layout)

        TabPage.setLayout(vertical_layout)
        return TabPage

    def top_layout(self, idx):
        """Function to clearly distinguish between the different layouts.
        It contains the label for the name of the launch service provider,
        and the layout of the corresponding label.

        Args:
            idx ([int]): Index of entry in the results array.

        Returns:
            [QVBoxLayout]: A vertical box layout containing the label of
            the launch service provider.
        """
        launch_service_provider = self.data.get_launch_service_provider(idx)

        layout = QVBoxLayout()
        launch_service_provider_label = QLabel()
        launch_service_provider_label.setText(f"{launch_service_provider}")
        launch_service_provider_label.setAlignment(QtCore.Qt.AlignCenter)
        launch_service_provider_label.setFont(
            QtGui.QFont("Times", weight=QtGui.QFont.Bold, pointSize=24)
        )

        layout.addWidget(launch_service_provider_label)
        return layout

    def left_layout(self, idx):
        """Function to clearly distinguish between the different layouts.
        It contains the label for the different information available to the
        mission. It also contains the formatting of the label.

        Args:
            idx ([int]): Index of entry in the results array.

        Returns:
            [QVBoxLayout]: A vertical box layout containing mission
            information.
        """
        launch_name = self.data.get_launch_name(idx)
        launch_status = self.data.get_launch_status_abbrev(idx)
        launch_description = self.data.get_launch_description(idx)

        # F-strings don't like it when you use \ inside them,
        # so we do this work around.
        double_nl = '\n\n'

        layout = QVBoxLayout()
        mission_info = QLabel()
        mission_info.setText(
            f"The {launch_name} has status: "
            f"{launch_status}{double_nl}{launch_description}"
        )
        mission_info.setWordWrap(True)
        mission_info.setAlignment(QtCore.Qt.AlignTop)

        layout.addWidget(mission_info)
        return layout

    def right_layout(self, idx):
        """Function to clearly distinguish between the different layouts.
        It includes a folium map showing the location of the launch pad.

        Args:
            idx ([int]): Index of entry in the results array.

        Returns:
            [QVBoxLayout]: A vertical box layout containing the map.
        """
        self.view = QtWebEngineWidgets.QWebEngineView()
        lon = float(self.data.get_longitude(idx))
        lat = float(self.data.get_latitude(idx))

        layout = QVBoxLayout()
        # Make a folium map with the longitude and latitude from the data
        map_location = folium.Map(
            location=[lat, lon],
            tiles="Stamen Toner",
            zoom_start=3
        )

        # To actually display this map we need to decode the information. The
        # exact details how and why are not know to me but the source for this:
        # https://stackoverflow.com/questions/60437182/how-to-include-folium-map-into-pyqt5-application-window
        data = io.BytesIO()
        map_location.save(data, close_file=False)
        self.view.setHtml(data.getvalue().decode())

        layout.addWidget(self.view)
        return layout

if __name__ == "__main__":
    App = QtWidgets.QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(App.exec())

