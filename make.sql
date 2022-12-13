-- MySQL dump 10.13  Distrib 8.0.31, for macos12.6 (arm64)
--
-- Host: 103.3.61.112    Database: icabroad
-- ------------------------------------------------------
-- Server version	8.0.31-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `approved_course`
--

DROP TABLE IF EXISTS `approved_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `approved_course` (
  `id` int NOT NULL AUTO_INCREMENT,
  `n_id` int NOT NULL,
  `c_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_approval` (`n_id`,`c_id`),
  KEY `approved_course_ic_course_null_fk` (`c_id`),
  CONSTRAINT `approved_course_ic_course_null_fk` FOREIGN KEY (`c_id`) REFERENCES `ic_course` (`c_id`),
  CONSTRAINT `approved_course_partner_course_null_fk` FOREIGN KEY (`n_id`) REFERENCES `partner_course` (`n_id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `country`
--

DROP TABLE IF EXISTS `country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `country` (
  `country_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `continent` varchar(255) NOT NULL,
  PRIMARY KEY (`country_id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `faq`
--

DROP TABLE IF EXISTS `faq`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faq` (
  `id` int NOT NULL AUTO_INCREMENT,
  `question` varchar(255) DEFAULT NULL,
  `answer` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ic_course`
--

DROP TABLE IF EXISTS `ic_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ic_course` (
  `c_id` int NOT NULL AUTO_INCREMENT,
  `ic_cid` varchar(255) NOT NULL,
  `ic_name` varchar(255) NOT NULL,
  `credits` int NOT NULL,
  `major` enum('Marketing','International Business','Finance','Business Economics','Computer Engineering','Creative Technology','Physics','Food Science and Technology','Computer Science','Chemistry','Biological Science','Applied Mathematics','Communication Design','Media and Communication','Intercultural Studies and Languages','International Relations and Global Affairs','Travel and Service Business Entrepreneurship') DEFAULT NULL,
  PRIMARY KEY (`c_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `links`
--

DROP TABLE IF EXISTS `links`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `links` (
  `link_id` int NOT NULL AUTO_INCREMENT,
  `link_name` varchar(255) NOT NULL,
  `url` tinytext NOT NULL,
  PRIMARY KEY (`link_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `partner_course`
--

DROP TABLE IF EXISTS `partner_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `partner_course` (
  `n_id` int NOT NULL AUTO_INCREMENT,
  `pn_cid` varchar(255) NOT NULL,
  `pn_name` varchar(255) DEFAULT NULL,
  `credits` int DEFAULT NULL,
  `major` varchar(255) DEFAULT NULL,
  `uni_id` int NOT NULL,
  PRIMARY KEY (`n_id`),
  UNIQUE KEY `n_id` (`n_id`),
  KEY `partner_course_partner_university_null_fk` (`uni_id`),
  CONSTRAINT `partner_course_partner_university_null_fk` FOREIGN KEY (`uni_id`) REFERENCES `partner_university` (`uni_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `partner_university`
--

DROP TABLE IF EXISTS `partner_university`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `partner_university` (
  `uni_id` int NOT NULL AUTO_INCREMENT,
  `uni_name` varchar(255) NOT NULL,
  `country_id` int NOT NULL,
  `required_gpa` float DEFAULT NULL,
  `housing_type` int DEFAULT NULL,
  `est_cost_max` int DEFAULT NULL,
  `est_cost_min` int DEFAULT NULL,
  `map_link` varchar(255) DEFAULT NULL,
  `incoming_stu_link` varchar(255) DEFAULT NULL,
  `course_open_link` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`uni_id`),
  UNIQUE KEY `uni_name` (`uni_name`),
  KEY `partner_university_country_null_fk` (`country_id`),
  CONSTRAINT `partner_university_country_null_fk` FOREIGN KEY (`country_id`) REFERENCES `country` (`country_id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-12-13 11:41:13
