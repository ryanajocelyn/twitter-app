import axios from 'axios';

export function login() {
    return axios.get(`/api/v1/tweets/search?userId=67001092`);
}

export function syncTweets(userId) {
    return axios.get(`/api/v1/users/sync/tweets?userId=${userId}`);
}
