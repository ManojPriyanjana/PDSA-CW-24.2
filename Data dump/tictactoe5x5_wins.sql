-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: tictactoe5x5
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
-- Table structure for table `wins`
--

DROP TABLE IF EXISTS `wins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wins` (
  `id` int NOT NULL AUTO_INCREMENT,
  `player` varchar(100) DEFAULT NULL,
  `board_state` text,
  `won_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wins`
--

LOCK TABLES `wins` WRITE;
/*!40000 ALTER TABLE `wins` DISABLE KEYS */;
INSERT INTO `wins` VALUES (1,'kasun','[[\"X\", \"O\", \" \", \" \", \" \"], [\" \", \"X\", \" \", \" \", \" \"], [\" \", \" \", \"X\", \"O\", \" \"], [\"O\", \" \", \"O\", \"X\", \" \"], [\" \", \" \", \" \", \" \", \"X\"]]','2025-04-29 10:25:14'),(2,'Eranda','[[\" \", \" \", \"X\", \"X\", \" \"], [\"O\", \"X\", \"X\", \"O\", \" \"], [\"O\", \" \", \"X\", \"X\", \"O\"], [\"O\", \"O\", \"X\", \" \", \" \"], [\" \", \" \", \"X\", \"O\", \" \"]]','2025-04-29 10:28:14'),(3,'Tharidu','[[\"X\", \"O\", \"O\", \"O\", \" \"], [\" \", \"X\", \" \", \" \", \"O\"], [\" \", \" \", \"X\", \" \", \" \"], [\" \", \" \", \" \", \"X\", \" \"], [\" \", \" \", \" \", \" \", \"X\"]]','2025-04-29 10:32:15'),(4,'Tharidu','[[\"X\", \"O\", \"O\", \"O\", \" \"], [\" \", \"X\", \" \", \" \", \"O\"], [\" \", \" \", \"X\", \" \", \" \"], [\" \", \" \", \" \", \"X\", \"X\"], [\" \", \" \", \" \", \" \", \"X\"]]','2025-04-29 10:32:19');
/*!40000 ALTER TABLE `wins` ENABLE KEYS */;
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
