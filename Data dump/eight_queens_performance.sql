-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: eight_queens
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
-- Table structure for table `performance`
--

DROP TABLE IF EXISTS `performance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `performance` (
  `id` int NOT NULL AUTO_INCREMENT,
  `mode` varchar(16) DEFAULT NULL,
  `duration` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `performance`
--

LOCK TABLES `performance` WRITE;
/*!40000 ALTER TABLE `performance` DISABLE KEYS */;
INSERT INTO `performance` VALUES (1,'Sequential',0.001537),(2,'Threaded',0.005679),(3,'Sequential',0.0015548),(4,'Threaded',0.0055224),(5,'Sequential',0.0015987),(6,'Threaded',0.0057724),(7,'Sequential',0.0015755),(8,'Threaded',0.0050838),(9,'Sequential',0.001634),(10,'Threaded',0.0043588),(11,'Sequential',0.0015884),(12,'Threaded',0.0044557),(13,'Sequential',0.0016127),(14,'Threaded',0.0061639),(15,'Sequential',0.0015796),(16,'Threaded',0.0057809),(17,'Sequential',0.0016122),(18,'Threaded',0.0039926),(19,'Sequential',0.0016137),(20,'Threaded',0.0037959),(21,'Sequential',0.0015716),(22,'Threaded',0.00589),(23,'Sequential',0.0016066),(24,'Threaded',0.004781),(25,'Sequential',0.0015939),(26,'Threaded',0.004116),(27,'Sequential',0.0015935),(28,'Threaded',0.0046485),(29,'Sequential',0.0015808),(30,'Threaded',0.0040552),(31,'Sequential',0.001624),(32,'Threaded',0.0044831),(33,'Sequential',0.0016136),(34,'Threaded',0.0055134),(35,'Sequential',0.0016315),(36,'Threaded',0.0045045),(37,'Sequential',0.0015757),(38,'Threaded',0.0045673),(39,'Sequential',0.0015984),(40,'Threaded',0.0046649),(41,'Sequential',0.0016203),(42,'Threaded',0.0040897),(43,'Sequential',0.001556),(44,'Threaded',0.0049203),(45,'Sequential',0.0016013),(46,'Threaded',0.0044114),(47,'Sequential',0.0016077),(48,'Threaded',0.0053345),(49,'Sequential',0.0016218),(50,'Threaded',0.0045277),(51,'Sequential',0.0015773),(52,'Threaded',0.0043274),(53,'Sequential',0.0016121),(54,'Threaded',0.004849),(55,'Sequential',0.0016369),(56,'Threaded',0.0040678),(57,'Sequential',0.0016256),(58,'Threaded',0.0043549),(59,'Sequential',0.0015934),(60,'Threaded',0.0041792),(61,'Sequential',0.0015834),(62,'Threaded',0.0037711),(63,'Sequential',0.0015843),(64,'Sequential',0.0017466),(65,'Threaded',0.0041294),(66,'Threaded',0.0047057),(67,'Sequential',0.0016646),(68,'Threaded',0.0044069),(69,'Sequential',0.0015827),(70,'Sequential',0.00162),(71,'Threaded',0.0042146),(72,'Threaded',0.0042585),(73,'Sequential',0.0015764),(74,'Threaded',0.0048089),(75,'Sequential',0.0015887),(76,'Threaded',0.0054338),(77,'Sequential',0.0016903),(78,'Threaded',0.0051899),(79,'Sequential',0.0016274),(80,'Threaded',0.0055337);
/*!40000 ALTER TABLE `performance` ENABLE KEYS */;
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
