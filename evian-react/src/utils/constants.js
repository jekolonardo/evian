import os from "os";

// export const hostname =  "192.168.137.1";
export const hostname =  os.hostname();

export const mediaPrefix = `http://${hostname}:8000/media/client/`;

export const STUDENT = "student";
export const STAFF = "staff";

export const COURSES = [
  { name: "Advanced Software Engineering", code: "CZ3002", group: "TS4" }
];

export const ATTENDANCE = [
  {
    index: "16604",
    type: "lab",
    date: "08-09-19",
    time: "10:30",
    duration: "1 hour",
    status: "present"
  },
  {
    index: "15604",
    type: "tut",
    date: "09-09-19",
    time: "10:30",
    duration: "1 hour",
    status: "present"
  }
];

export const LAB_STATS = [
  { index: "11030", rate: "45/46", date: "09-04-19", time: "1030" },
  { index: "11030", rate: "45/46", date: "09-04-19", time: "1030" },
  { index: "11030", rate: "45/46", date: "09-04-19", time: "1030" },
  { index: "11030", rate: "45/46", date: "09-04-19", time: "1030" },
  { index: "11030", rate: "45/46", date: "09-04-19", time: "1030" },
  { index: "11030", rate: "45/46", date: "09-04-19", time: "1030" }
];

export const TUT_STATS = [
  { index: "11030", rate: "45/46", date: "09-04-19", time: "1030" },
  { index: "11030", rate: "45/46", date: "09-04-19", time: "1030" },
  { index: "11030", rate: "45/46", date: "09-04-19", time: "1030" },
  { index: "11030", rate: "45/46", date: "09-04-19", time: "1030" },
  { index: "11030", rate: "45/46", date: "09-04-19", time: "1030" },
  { index: "11030", rate: "45/46", date: "09-04-19", time: "1030" },
  { index: "11030", rate: "45/46", date: "09-04-19", time: "1030" },
  { index: "11030", rate: "45/46", date: "09-04-19", time: "1030" },
  { index: "11030", rate: "45/46", date: "09-04-19", time: "1030" },
  { index: "11030", rate: "45/46", date: "09-04-19", time: "1030" },
  { index: "11030", rate: "45/46", date: "09-04-19", time: "1030" },
  { index: "11030", rate: "45/46", date: "09-04-19", time: "1030" }
];

export const SESSION_ATTENDANCE = [
  {
    name: "Andrew",
    matric: "U1620493L",
    status: "absent",
    index: "15093",
    time: "08-04-19"
  },
  {
    name: "See",
    matric: "U1620593L",
    status: "mc",
    index: "15093",
    time: "08-04-19"
  },
  {
    name: "Lee",
    matric: "U1620693L",
    status: "present",
    index: "15093",
    time: "08-04-19"
  },
  {
    name: "Mark",
    matric: "U1620483L",
    status: "present",
    index: "15093",
    time: "08-04-19"
  },
  {
    name: "David",
    matric: "U1620413L",
    status: "present",
    index: "15093",
    time: "08-04-19"
  },
  {
    name: "Andrew",
    matric: "U1620493L",
    status: "absent",
    index: "15093",
    time: "08-04-19"
  },
  {
    name: "See",
    matric: "U1620593L",
    status: "mc",
    index: "15093",
    time: "08-04-19"
  },
  {
    name: "Lee",
    matric: "U1620693L",
    status: "present",
    index: "15093",
    time: "08-04-19"
  },
  {
    name: "Mark",
    matric: "U1620483L",
    status: "present",
    index: "15093",
    time: "08-04-19"
  },
  {
    name: "David",
    matric: "U1620413L",
    status: "present",
    index: "15093",
    time: "08-04-19"
  }
];
