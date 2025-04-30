-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: hanoi_stats
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
-- Table structure for table `player_solutions`
--

DROP TABLE IF EXISTS `player_solutions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_solutions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `timestamp` datetime DEFAULT NULL,
  `player_name` varchar(100) DEFAULT NULL,
  `game_type` varchar(10) DEFAULT NULL,
  `moves` int DEFAULT NULL,
  `sequence` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `player_solutions`
--

LOCK TABLES `player_solutions` WRITE;
/*!40000 ALTER TABLE `player_solutions` DISABLE KEYS */;
INSERT INTO `player_solutions` VALUES (1,'2025-04-30 13:30:09','manoj','3-peg',37,'A->C,A->B,C->B,A->C,B->A,B->C,A->C,A->B,C->B,C->A,B->A,C->B,A->C,A->B,C->B,A->C,B->A,B->C,A->B,C->A,B->A,B->C,A->C,A->B,C->B,C->A,B->C,B->A,C->A,B->C,A->C,A->B,C->B,A->C,B->A,B->C,A->C'),(2,'2025-04-30 13:32:10','manoj','4-peg',22,'A->C,A->D,C->D,A->B,A->C,B->A,C->B,A->B,D->C,D->B,C->B,A->D,B->D,B->C,D->C,B->A,B->D,A->B,B->D,C->B,C->D,B->D'),(3,'2025-04-30 20:10:05','manoj','3-peg',58,'A->B,A->C,B->C,A->B,C->A,A->B,B->A,C->B,A->B,A->C,B->A,A->C,C->A,B->C,A->C,B->A,C->B,C->A,B->A,C->B,A->C,A->B,C->B,B->C,B->A,A->B,C->A,B->C,A->C,A->B,C->A,C->B,A->B,A->C,B->A,B->C,A->C,C->A,A->B,B->A,C->B,A->C,B->A,C->B,A->C,B->C,B->A,C->B,C->A,B->A,B->C,A->C,A->B,C->B,A->C,B->A,B->C,A->C'),(4,'2025-04-30 21:03:44','manoj','3-peg',99,'A->B,A->C,B->C,A->B,C->B,C->A,B->A,B->C,A->B,A->C,B->C,A->B,C->A,C->B,A->B,C->A,B->C,B->A,C->A,B->C,A->B,A->C,B->C,A->B,C->A,C->B,B->C,A->B,B->C,B->A,C->B,B->C,C->A,C->B,A->B,A->C,B->A,B->C,A->C,A->B,C->A,C->B,A->B,C->A,B->C,B->A,C->A,C->B,A->B,A->C,B->C,A->B,C->A,C->B,A->B,A->C,B->A,B->C,A->C,B->A,C->B,C->A,B->A,B->C,A->B,A->C,B->C,A->B,C->A,C->B,A->B,C->A,B->C,B->A,C->B,A->C,B->C,B->A,C->B,C->A,B->A,B->C,A->B,A->C,B->C,A->B,C->A,C->B,A->B,A->C,B->C,B->A,C->A,B->C,A->C,A->B,C->A,B->C,A->C');
/*!40000 ALTER TABLE `player_solutions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-30 22:24:24
