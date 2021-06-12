import axios from 'axios';

export function fetchTimeline(criteria = { count: 50 }) {
    let fetchUrl = `/api/v1/tweets/search?userId=${criteria.userId}`;
    if (criteria.startDate) {
        fetchUrl = `${fetchUrl}&start_date=${criteria.startDate}`;
    }
    if (criteria.endDate) {
        fetchUrl = `${fetchUrl}&end_date=${criteria.endDate}`;
    }

    return axios.get(fetchUrl);
}

export function syncTimeline(userId) {
    return axios.get(`/api/v1/users/sync/timeline?userId=${userId}`);
}
