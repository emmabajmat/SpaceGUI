import os
import time
import json
import requests


class DataFetcher():
    """DataFetcher class responsible for passing data. The class reads a JSON
    file if it was retrieved from the API less than 12 hours ago. If not, a new
    JSON is downloaded and stored.
    """

    def __init__(self):
        """Initialize the DataFetcher Class."""
        self.url = (
            "https://ll.thespacedevs.com/2.2.0/launch/upcoming/"
            "?&include_suborbital=true&related=false&hide_recent_previous=True"
        )
        self.json = self.get_json_data()
        self.results = self.json['results']

    def get_data_from_url(self):
        """Downloads data from the API and stores it in a new JSON file."""
        req = requests.get(self.url)
        with open('tmp_launch_data.json', 'w') as f:
            f.write(req.text)

        # Rename the temporary file to a filename with the current timestamp
        os.rename(
            'tmp_launch_data.json', f'launch_data_{round(time.time())}.json'
        )

    def select_data(self):
        """Selects which data to return. If the data is older than 12 hours,
        a new call is made to the API. Otherwise, the current JSON is returned.

        Returns:
            [str]: Name of the JSON file with launch data.
        """
        cwd_files = os.listdir(os.getcwd())

        # Find the file that end with .json
        data_file = [json for json in cwd_files if json.endswith('.json')][-1]

        # Retrieve the timestamp part of the name of the file
        # Cuts the .json part and the launch_data of and make it an int
        old_timestamp = int(data_file.split("_", 2)[2:][0][:-5])

        # If atleast a 12 hours passed since the last data file was retrieved,
        # fetch new data from url and rerun this function
        if time.time() - old_timestamp > 3600 * 12:
            self.get_data_from_url()
            data_file = [json for json in cwd_files if json.endswith('.json')][-1]

        return data_file

    def get_json_data(self):
        """Returns a JSON formatted string with the latest launch data.

        Returns:
            [dict]: JSON formatted string.
        """
        with open(self.select_data(), 'r') as f:
            data = f.read()
        return json.loads(data)

    def get_results_length(self):
        """Returns the length of the results array.

        Returns:
            [int]: Length of results array.
        """
        return len(self.data['results'])

    def get_launch_service_provider(self, idx):
        """Get the name of the launch service provider.

        Args:
            idx ([int]): Index of entry in the results array.

        Returns:
            [str]: Name of the launch service provider
        """
        return self.results[idx]["launch_service_provider"]["name"]

    def get_launch_name(self, idx):
        """Get the launch name

        Args:
            idx ([int]): Index of entry in the results array.

        Returns:
            [str]: Name of the launch
        """
        return self.results[idx]["name"]

    def get_launch_status_abbrev(self, idx):
        """Get the abbreviation of the launch status.

        Args:
            idx ([int]): Index of entry in the results array.

        Returns:
            [str]: The abbreviation of the launch status
        """
        return self.results[idx]["status"]["abbrev"]

    def get_launch_window(self, idx):
        """Get the start and end of the launch window.

        Args:
            idx ([int]): Index of entry in the results array.

        Returns:
            [tuple]: Tuple containing the start and end of the launch window
        """
        start = self.results[idx]["window_start"]
        end = self.results[idx]["window_end"]
        return (start, end)

    def get_launch_description(self, idx):
        """Get a description of the launch.

        Args:
            idx ([int]): Index of entry in the results array.

        Returns:
            [str]: Description of the launch.
        """
        return self.results[idx]["mission"]["description"]

    def get_longitude(self, idx):
        """Get the longitude of the launch location.

        Args:
            idx ([int]): Index of entry in the results array.

        Returns:
            [str]: Longitude of the launch location.
        """
        return self.results[idx]["pad"]["longitude"]

    def get_latitude(self, idx):
        """Get the latitude of the launch location.

        Args:
            idx ([int]): Index of entry in the results array.

        Returns:
            [str]: Latitude of the launch location.
        """
        return self.results[idx]["pad"]["latitude"]

