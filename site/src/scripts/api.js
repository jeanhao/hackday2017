const BASE_API = '/'

export default {
  sign: `${BASE_API}api/user/register`,
  login: `${BASE_API}api/user/login`,
  getVertifyCode: `${BASE_API}api/user/message`,
  plantList: `${BASE_API}api/plant/list`,
  getTags: `${BASE_API}api/task/tag/list`,
  getProblems: `${BASE_API}api/task/problem/list`,
  getAnswers: `${BASE_API}api/task/problem/answer`,
  startPlan: `${BASE_API}api/task/answer/confirm`,
}
