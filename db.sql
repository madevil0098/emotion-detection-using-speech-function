create database smarteye;

create table smarteye.session(
    session_id varchar(36),
    session_title varchar(100) NOT NULL,
    session_date date NOT NULL,
    session_start_time time NOT NULL,
    clusteringDone boolean default false, 
    analysisDone boolean default false, 
    noOfCluster int default NULL, 
    PRIMARY KEY(session_id)
);