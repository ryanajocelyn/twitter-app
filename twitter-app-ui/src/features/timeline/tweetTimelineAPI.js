import axios from 'axios';

export function fetchTimeline(count = 50) {
    return axios.get(`/api/v1/tweets/search?userId=67001092`);
}

export function syncTimeline(userId) {
    return axios.get(`/api/v1/users/sync/timeline?userId=${userId}`);
}
