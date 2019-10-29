import axios from "../utils/AxiosPlugin";

export const PostFacialAPI = async params => {
  return await axios.post(`facial/`, params);
};

export const PostLoginAPI = async params => {
  return await axios.post(`login/`, params);
};

export const PostAttendanceAPI = async params => {
  return await axios.post(`attendance/`, params);
};

export const PostCourstStatsAPI = async params => {
  return await axios.post(`course-stats/`, params);
};

export const PostSessionAttendanceAPI = async params => {
  return await axios.post(`session-attendance/`, params);
};

export const PostOverwriteAPI = async params => {
  return await axios.post(`overwrite/`, params);
};
