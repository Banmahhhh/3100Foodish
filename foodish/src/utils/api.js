const root = "";
export const LOGIN = `${root}/logintoken/`;
export const REGISTER = `${root}/api/userregister/`;
export const FOOD = `${root}/api/foods/`;
export const FOOD_LIST = `${root}/api/foods/`;
export const FOOD_INFO = id => `${root} /api/foods/${id}/`;
export const USER_LIST = username => `${root}/api/users/?username=${username}`;
export const FOOD_DELETE = id => `${root}/api/foods/${id}/`;
export const BOOK = `${root}/api/books/`;
export const BOOK_LIST_Q = id => `${root}/api/books/?user=${id}`;
export const BOOK_DEL = id => `${root}/api/books/${id}/`;
export const COMMIT_ADD = `${root}/api/comments/`;
export const IMAGE_UPLOAD = `${root}/upload/image/`;
export const UPDATE_USER = id => `${root}/api/users/${id}/`;
export const FOOD_UPDATE = id => `${root}/api/foods/${id}/`;
export const REMAD_LIST = `${root}/api/recommend/`;
export const USER_D_INFO = id => `${root}/api/users/${id}/`;
export const CHECK_FOLLOW = `${root}/api/check_follow/`;
export const FOLLOW = `${root}/api/follow/`;
export const COMPLAIN = `${root}/api/complain/`;
export const NOTIFY = `${root}/api/notify/`;
