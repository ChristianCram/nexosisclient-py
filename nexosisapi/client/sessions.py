from nexosisapi.session import SessionResult, SessionResponse
from nexosisapi.time_interval import TimeInterval


class Sessions(object):
    """Session based API operations"""
    def __init__(self, client):
        self._client = client

    def _create_session(self, dataset_name, action_type, target_column, event_name,
                        start_date, end_date, result_interval, is_estimate=False, column_metadata=None,
                        callback_url=None):
        return self._client.request_with_headers('POST', 'sessions/%s' % action_type,
                                                 params={
                                        'dataSetName': dataset_name,
                                        'targetColumn': target_column,
                                        'eventName': event_name,
                                        'startDate': start_date,
                                        'endDate': end_date,
                                        'isEstimate': is_estimate,
                                        'resultInterval': result_interval.name,
                                        'callbackUrl': callback_url},
                                                 data={
                                        'dataSetName': dataset_name,
                                        'columns': column_metadata
                                    })


    def create_forecast(self, dataset_name, target_column, start_date, end_date, result_interval=TimeInterval.day,
                        callback_url=None):
        """Create a new forecast for a dataset

        :param str dataset_name: the name of the dataset to forecast on
        :param str target_column: the column from the dataset to forecast over
        :param datetime start_date: the first datetime of the forecast
        :param datetime end_date: the last datetime of the forecast
        :param TimeInterval result_interval: the interval between predictions in the results
        :param str callback_url: the url to callback to on session status change events

        :return the session description
        :rtype: SessionResponse
        """
        response, _, headers = self._create_session(dataset_name, 'forecast', target_column, None, start_date, end_date,
                                                    result_interval, callback_url=callback_url)
        return SessionResponse(response, headers)

    def analyze_impact(self, dataset_name, target_column, event_name, start_date, end_date,
                       result_interval=TimeInterval.day, callback_url=None):
        """Create a new impact analysis on a dataset

        :param str dataset_name: the name of the dataset to forecast on
        :param str target_column: the column from the dataset to forecast over
        :param str event_name: the name of this analysis
        :param datetime start_date: the first datetime of the forecast
        :param datetime end_date: the last datetime of the forecast
        :param TimeInterval result_interval: the interval between predictions in the results
        :param str callback_url: the url to callback to on session status change events

        :return the session description
        :rtype: SessionResponse
        """
        response, _, headers = self._create_session(dataset_name, 'impact', target_column, event_name, start_date,
                                                    end_date,
                                                    result_interval, callback_url=callback_url)
        return SessionResponse(response, headers)

    def estimate_forecast(self, dataset_name, target_column, start_date, end_date, result_interval=TimeInterval.day):
        """Estimate a new forecast for a dataset

        :param str dataset_name: the name of the dataset to forecast on
        :param str target_column: the column from the dataset to forecast over
        :param datetime start_date: the first datetime of the forecast
        :param datetime end_date: the last datetime of the forecast
        :param TimeInterval result_interval: the interval between predictions in the results

        :return the session description
        :rtype: SessionResponse
        """
        response, _, headers = self._create_session(dataset_name, 'forecast', target_column, None, start_date, end_date,
                                                    result_interval, is_estimate=True)
        return SessionResponse(response, headers)

    def estimate_impact(self, dataset_name, target_column, event_name, start_date, end_date,
                        result_interval=TimeInterval.day):
        """Estimate an impact analysis on a dataset

        :param str dataset_name: the name of the dataset to forecast on
        :param str target_column: the column from the dataset to forecast over
        :param str event_name: the name of this analysis
        :param datetime start_date: the first datetime of the forecast
        :param datetime end_date: the last datetime of the forecast
        :param TimeInterval result_interval: the interval between predictions in the results

        :return the session description
        :rtype: SessionResponse
        """
        response, _, headers = self._create_session(dataset_name, 'impact', target_column, event_name, start_date,
                                                    end_date,
                                                    result_interval, is_estimate=True)
        return SessionResponse(response, headers)

    def list(self, dataset_name=None, event_name=None, requested_after=None, requested_before=None, session_type=None):
        """list the created sessions, optionally filtering on session parameters

        :param str dataset_name: filter on the name of the dataset used
        :param str event_name: filter on the event name given when running an impact analysis
        :param datetime requested_before: only include sessions created before this date
        :param datetime requested_after: only include sessions created after this date
        :param SessionType session_type: filter on the type of session

        :returns a list of :class:`SessionResponses`
        :rtype list
        """
        query = {
            'dataSetName': dataset_name,
            'eventName': event_name,
            'requestedBefore': requested_before,
            'requestedAfter': requested_after,
            'sessionType': session_type
        }
        response, _, headers = self._client.request_with_headers('GET', 'sessions', params=query)

        return [SessionResponse(item, headers) for item in response.get('items', [])]


    def remove(self, session_id):
        """Remove a session based on the session id

        :param str session_id: the session to remove
        """
        self._client.request('DELETE', 'sessions/%s' % session_id)

    def remove_sessions(self, **kwargs):
        self._client.request('DELETE', 'sessions', params=kwargs)

    def get_results(self, session_id):
        """Get the results of a session based on the session id

        :param str session_id: the session to get results for

        :returns the results of computation run by the session
        :rtype SessionResult
        """
        response = self._client.request('GET', 'sessions/%s/results' % session_id)
        return SessionResult(response)

    def get(self, session_id):
        """Get a session based on the session id

        :param str session_id: the session to get

        :returns the information about the session
        :rtype SessionResponse
        """
        response, _, headers = self._client.request_with_headers('GET', 'sessions/%s' % session_id)
        return SessionResponse(response, headers)
