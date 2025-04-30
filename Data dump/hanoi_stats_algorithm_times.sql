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
-- Table structure for table `algorithm_times`
--

DROP TABLE IF EXISTS `algorithm_times`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `algorithm_times` (
  `id` int NOT NULL AUTO_INCREMENT,
  `timestamp` datetime DEFAULT NULL,
  `game_type` varchar(10) DEFAULT NULL,
  `algorithm` varchar(20) DEFAULT NULL,
  `disks` int DEFAULT NULL,
  `duration` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `algorithm_times`
--

LOCK TABLES `algorithm_times` WRITE;
/*!40000 ALTER TABLE `algorithm_times` DISABLE KEYS */;
INSERT INTO `algorithm_times` VALUES (1,'2025-04-30 13:30:09','3-peg','3-recursive',5,0.000014543533325195312),(2,'2025-04-30 13:30:09','3-peg','3-iterative',5,0.00007271766662597656),(3,'2025-04-30 13:32:10','4-peg','4-recursive',5,0.00001621246337890625),(4,'2025-04-30 13:32:10','4-peg','4-iterative',5,0.00006008148193359375),(5,'2025-04-30 20:10:05','3-peg','3-recursive',5,0.000014781951904296875),(6,'2025-04-30 20:10:05','3-peg','3-iterative',5,0.00006437301635742188),(7,'2025-04-30 21:03:44','3-peg','3-recursive',6,0.00003123283386230469),(8,'2025-04-30 21:03:44','3-peg','3-iterative',6,0.00010132789611816406);
/*!40000 ALTER TABLE `algorithm_times` ENABLE KEYS */;
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
