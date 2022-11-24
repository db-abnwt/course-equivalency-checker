create schema ic_abroad_in_db;

CREATE TABLE partner_university
(
    uni_id            int primary key AUTO_INCREMENT,
    uni_name          varchar(255),
    country_id        int,
    required_gpa      float        null,
    housing_type      int          null,
    est_cost_max      int          null,
    est_cost_min      int          null,
    map_link          varchar(255) null,
    incoming_stu_link varchar(255) null,
    course_open_link  varchar(255) null
);

CREATE TABLE country
(
    country_id int primary key AUTO_INCREMENT,
    `name`     varchar(255) not null,
    continent  varchar(255) not null
);

CREATE TABLE ext_scholarship
(
    id     int primary key AUTO_INCREMENT,
    `name` varchar(255) null,
    `desc` varchar(255) null
);

CREATE TABLE faq
(
    id       int primary key AUTO_INCREMENT,
    question varchar(255) null,
    answer   varchar(255) null
);

CREATE TABLE approved_course
(
    id      int primary key AUTO_INCREMENT,
    uni_id  int          not null,
    pn_cid  varchar(255) not null,
    ic_cid  varchar(255) not null,
    pn_name varchar(255) not null,
    credits varchar(255) not null
);

CREATE TABLE ic_course
(
    ic_cid  varchar(255) primary key,
    ic_name varchar(255) not null,
    credits int          not null,
    major   ENUM (
        'Marketing', 'International Business',
        'Finance', 'Business Economics',
        'Computer Engineering', 'Creative Technology',
        'Physics', 'Food Science and Technology',
        'Computer Science', 'Chemistry',
        'Biological Science', 'Applied Mathematics',
        'Communication Design', 'Media and Communication',
        'Intercultural Studies and Languages',
        'International Relations and Global Affairs',
        'Travel and Service Business Entrepreneurship'
        )
);
