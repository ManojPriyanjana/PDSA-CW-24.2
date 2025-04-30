-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: tsp_game_db
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `game_records`
--

DROP TABLE IF EXISTS `game_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `game_records` (
  `id` int NOT NULL AUTO_INCREMENT,
  `player_name` varchar(100) DEFAULT NULL,
  `home_city` char(1) DEFAULT NULL,
  `selected_cities` varchar(255) DEFAULT NULL,
  `algorithm` varchar(50) DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
  `distance` int DEFAULT NULL,
  `time_taken` float DEFAULT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_records`
--

LOCK TABLES `game_records` WRITE;
/*!40000 ALTER TABLE `game_records` DISABLE KEYS */;
INSERT INTO `game_records` VALUES (1,'manoj','B','H,I,J','Greedy','B-J-I-H-B',292,0.0000499,'2025-04-29 22:26:19'),(2,'manoj','B','H,I,J','Greedy','B-J-I-H-B',292,0.0000221,'2025-04-29 22:26:19'),(3,'manoj','B','H,I,J','Dynamic Programming','B-H-I-J-B',292,0.0000771,'2025-04-29 22:26:29'),(4,'manoj','B','H,I,J','Brute Force','B-H-I-J-B',292,0.0000489,'2025-04-29 22:26:39'),(5,'manoj','F','A,D,F,G','Greedy','F-A-G-D-F',292,0.0000208,'2025-04-29 22:29:07'),(6,'manoj','F','A,D,F,G','Dynamic Programming','F-D-G-A-F',292,0.0000628,'2025-04-29 22:29:09'),(7,'manoj','F','A,D,F,G','Brute Force','F-D-G-A-F',292,0.0000422,'2025-04-29 22:29:10'),(8,'manoj','H','F,G,I','Greedy','H-G-F-I-H',307,0.0000255,'2025-04-29 22:31:11'),(9,'manoj','H','F,G,I','Brute Force','H-I-G-F-H',303,0.0000378,'2025-04-29 22:31:14'),(10,'manoj','H','F,G,I','Dynamic Programming','H-I-G-F-H',303,0.0000583,'2025-04-29 22:31:15'),(11,'manoj','E','G,H','Greedy','E-H-G-E',210,0.0000217,'2025-04-29 22:32:40'),(12,'manoj','E','G,H','Dynamic Programming','E-H-G-E',210,0.0000374,'2025-04-29 22:32:42'),(13,'manoj','E','G,H','Brute Force','E-H-G-E',210,0.0000304,'2025-04-29 22:32:44'),(14,'manoj','D','A,E,F,G,H','Greedy','D-G-E-A-H-F-D',394,0.0000255,'2025-04-29 22:34:47'),(15,'manoj','D','A,E,F,G,H','Dynamic Programming','D-F-H-A-E-G-D',394,0.0001921,'2025-04-29 22:34:49'),(16,'manoj','D','A,E,F,G,H','Brute Force','D-F-H-A-E-G-D',394,0.0002481,'2025-04-29 22:34:51'),(17,'manoj','C','D,E,H','Greedy','C-E-H-D-C',224,0.000019,'2025-04-29 22:35:20'),(18,'manoj','C','D,E,H','Dynamic Programming','C-E-H-D-C',224,0.0000558,'2025-04-29 22:35:21'),(19,'manoj','C','D,E,H','Brute Force','C-E-H-D-C',224,0.0000387,'2025-04-29 22:35:23'),(20,'manoj','A','A,B,E,H','Greedy','A-B-E-H-A',307,0.0000278,'2025-04-29 22:38:09'),(21,'manoj','A','A,B,E,H','Brute Force','A-E-H-B-A',286,0.0000396,'2025-04-29 22:38:23'),(22,'manoj','A','A,B,E,H','Dynamic Programming','A-E-H-B-A',286,0.0000622,'2025-04-29 22:38:32'),(23,'manoj','G','D,I,J','Greedy','G-I-D-J-G',276,0.0000202,'2025-04-29 22:39:00'),(24,'manoj','G','D,I,J','Dynamic Programming','G-I-D-J-G',276,0.0000538,'2025-04-29 22:39:02'),(25,'manoj','G','D,I,J','Brute Force','G-I-D-J-G',276,0.0000479,'2025-04-29 22:39:04'),(26,'manoj','I','F,G,H','Greedy','I-H-F-G-I',332,0.0000203,'2025-04-29 22:41:22'),(27,'manoj','I','F,G,H','Dynamic Programming','I-H-F-G-I',332,0.0000568,'2025-04-29 22:41:23'),(28,'manoj','I','F,G,H','Brute Force','I-H-F-G-I',332,0.0000385,'2025-04-29 22:41:25'),(29,'manoj','C','A,B,D,E','Greedy','C-B-A-E-D-C',371,0.0000282,'2025-04-29 22:43:00'),(30,'manoj','C','A,B,D,E','Dynamic Programming','C-D-E-A-B-C',371,0.0000984,'2025-04-29 22:43:02'),(31,'manoj','C','A,B,D,E','Brute Force','C-D-E-A-B-C',371,0.0001133,'2025-04-29 22:43:04');
/*!40000 ALTER TABLE `game_records` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-30 22:24:23
