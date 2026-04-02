-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: edustay1
-- ------------------------------------------------------
-- Server version	8.0.44

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
-- Table structure for table `bookings`
--

DROP TABLE IF EXISTS `bookings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `property_id` int NOT NULL,
  `booking_date` date DEFAULT NULL,
  `status` enum('requested','accepted','rejected','cancelled') DEFAULT 'requested',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `contact_shared` enum('yes','no') DEFAULT 'no',
  `payment_status` enum('pending','paid') DEFAULT 'pending',
  `payment_amount` decimal(10,2) DEFAULT NULL,
  `transaction_id` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookings`
--

LOCK TABLES `bookings` WRITE;
/*!40000 ALTER TABLE `bookings` DISABLE KEYS */;
INSERT INTO `bookings` VALUES (1,2,1,'2026-03-22','accepted','2026-03-22 18:15:15','yes','paid',500.00,'TXN1774252393904'),(2,2,2,'2026-03-23','accepted','2026-03-23 07:36:24','yes','paid',0.00,'TXN1774347435505'),(3,2,1,'2026-03-23','accepted','2026-03-23 10:58:11','yes','paid',0.00,'TXN1774937225341'),(4,2,2,'2026-03-31','accepted','2026-03-31 17:39:21','yes','pending',1800.00,NULL);
/*!40000 ALTER TABLE `bookings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facilities`
--

DROP TABLE IF EXISTS `facilities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facilities` (
  `id` int NOT NULL AUTO_INCREMENT,
  `facility_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facilities`
--

LOCK TABLES `facilities` WRITE;
/*!40000 ALTER TABLE `facilities` DISABLE KEYS */;
INSERT INTO `facilities` VALUES (1,'WiFi'),(2,'Water'),(3,'Parking'),(4,'Security'),(5,'Food Included');
/*!40000 ALTER TABLE `facilities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nearby_places`
--

DROP TABLE IF EXISTS `nearby_places`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nearby_places` (
  `id` int NOT NULL AUTO_INCREMENT,
  `property_id` int DEFAULT NULL,
  `place_type` varchar(50) DEFAULT NULL,
  `name` varchar(150) DEFAULT NULL,
  `latitude` decimal(10,8) DEFAULT NULL,
  `longitude` decimal(11,8) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nearby_places`
--

LOCK TABLES `nearby_places` WRITE;
/*!40000 ALTER TABLE `nearby_places` DISABLE KEYS */;
/*!40000 ALTER TABLE `nearby_places` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `properties`
--

DROP TABLE IF EXISTS `properties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `properties` (
  `id` int NOT NULL AUTO_INCREMENT,
  `provider_id` int NOT NULL,
  `property_type_id` int NOT NULL,
  `title` varchar(150) DEFAULT NULL,
  `description` text,
  `rent` decimal(10,2) DEFAULT NULL,
  `deposit` decimal(10,2) DEFAULT NULL,
  `total_capacity` int DEFAULT NULL,
  `available_capacity` int DEFAULT NULL,
  `address` text,
  `latitude` decimal(10,8) DEFAULT NULL,
  `longitude` decimal(11,8) DEFAULT NULL,
  `gender_allowed` enum('male','female','any') DEFAULT NULL,
  `status` enum('pending','approved','rejected') DEFAULT 'pending',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `properties`
--

LOCK TABLES `properties` WRITE;
/*!40000 ALTER TABLE `properties` DISABLE KEYS */;
INSERT INTO `properties` VALUES (1,4,2,'Arya Girls PG','Safe PG near college',4500.00,10000.00,20,20,'Kolhapur',16.70500000,74.24330000,'female','approved','2026-01-09 18:51:47'),(2,4,4,'Arya Mess','kk',1800.00,500.00,NULL,NULL,'Kasba Bawada',16.73140234,74.24110640,'any','approved','2026-01-10 07:09:19'),(3,1,2,'so',NULL,2500.00,2000.00,NULL,NULL,'kop',18.48606632,73.87867257,'any','approved','2026-02-08 17:07:13'),(4,1,1,'Dd','Description gshhs ggshsh vhhsh hhhsh',2000.00,1000.00,NULL,NULL,'Kolhapur',18.23333891,73.84565022,'male','approved','2026-02-08 17:55:22'),(5,4,1,'Neha\'s Rooms','This rooms are available for only the girls, All cleaned and Affordable rooms rent',5000.00,2000.00,NULL,NULL,'A/p - Kasba Bawda , Pinjar Galli , Kolhapur',16.73314774,74.24516357,'female','approved','2026-03-31 06:53:18'),(6,4,4,'Varun\'s Mess','',2000.00,1000.00,NULL,NULL,'A/p, Kasba Bawda, Pinjar Galli, Kolhapur',16.73996220,74.24354084,'any','approved','2026-03-31 07:01:40'),(7,4,4,'Anay\'s Mees','This mess is very clean and maintains hygienic foods',2000.00,1000.00,NULL,NULL,'A/p, Kasba Bawda, Pinjar Galli, Kolhapur',16.73996220,74.24354084,'any','pending','2026-03-31 07:01:40');
/*!40000 ALTER TABLE `properties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property_facilities`
--

DROP TABLE IF EXISTS `property_facilities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `property_facilities` (
  `id` int NOT NULL AUTO_INCREMENT,
  `property_id` int DEFAULT NULL,
  `facility_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property_facilities`
--

LOCK TABLES `property_facilities` WRITE;
/*!40000 ALTER TABLE `property_facilities` DISABLE KEYS */;
INSERT INTO `property_facilities` VALUES (4,4,3),(5,3,1),(6,3,2),(10,2,1),(11,2,2),(12,2,3),(13,2,4),(14,1,1),(15,1,2),(16,1,3),(17,1,4);
/*!40000 ALTER TABLE `property_facilities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property_images`
--

DROP TABLE IF EXISTS `property_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `property_images` (
  `id` int NOT NULL AUTO_INCREMENT,
  `property_id` int NOT NULL,
  `image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property_images`
--

LOCK TABLES `property_images` WRITE;
/*!40000 ALTER TABLE `property_images` DISABLE KEYS */;
INSERT INTO `property_images` VALUES (2,4,'1770616004_property_1770616003360.jpg'),(3,3,'1770616052_property_1770616052949.jpg'),(4,4,'1770617200_property_1770617201094.jpg'),(6,4,'1770699528_property_1770699529002.jpg'),(8,2,'1774939014_property_1774938995099.jpg'),(11,2,'1774939119_property_1774939101262.jpg'),(13,1,'1774939139_property_1774939123510.jpg'),(14,1,'1774939146_property_1774939130388.jpg'),(15,1,'1774939150_property_1774939135247.jpg'),(17,5,'1774940230_property_1774940211722.jpg'),(19,6,'1774940704_property_1774940664454.jpg'),(20,7,'1774940715_property_1774940653782.jpg');
/*!40000 ALTER TABLE `property_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property_types`
--

DROP TABLE IF EXISTS `property_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `property_types` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property_types`
--

LOCK TABLES `property_types` WRITE;
/*!40000 ALTER TABLE `property_types` DISABLE KEYS */;
INSERT INTO `property_types` VALUES (1,'Room'),(2,'Hostel'),(3,'PG'),(4,'Mess');
/*!40000 ALTER TABLE `property_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `provider_profiles`
--

DROP TABLE IF EXISTS `provider_profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `provider_profiles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `id_proof` varchar(255) DEFAULT NULL,
  `address` text,
  `is_verified` enum('yes','no') DEFAULT 'no',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `provider_profiles`
--

LOCK TABLES `provider_profiles` WRITE;
/*!40000 ALTER TABLE `provider_profiles` DISABLE KEYS */;
INSERT INTO `provider_profiles` VALUES (1,4,NULL,'Kasaba Bawada Kolhapur','yes');
/*!40000 ALTER TABLE `provider_profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int DEFAULT NULL,
  `property_id` int DEFAULT NULL,
  `rating` int DEFAULT NULL,
  `review` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (1,2,1,4,'It was a nice experience..','2026-03-23 10:26:08'),(2,2,2,5,'Excellent','2026-03-24 10:41:25');
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_profiles`
--

DROP TABLE IF EXISTS `student_profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student_profiles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `college_name` varchar(150) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `gender` enum('male','female','other') DEFAULT NULL,
  `aadhar_number` varchar(20) DEFAULT NULL,
  `pan_number` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_profiles`
--

LOCK TABLES `student_profiles` WRITE;
/*!40000 ALTER TABLE `student_profiles` DISABLE KEYS */;
INSERT INTO `student_profiles` VALUES (1,2,'DYPCET Bawada','Kolhapur','female','659559673137','AWMPC0789Q');
/*!40000 ALTER TABLE `student_profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `mobile` varchar(15) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('student','provider','admin') NOT NULL,
  `status` enum('active','inactive','blocked') DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `gender` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mobile` (`mobile`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Admin','admin@gmail.com','9999999999','scrypt:32768:8:1$HoI2doh7k0CmuQW7$096c6dcd20bbe02051b036bcf08b56f18f211c7cd542e03d07c10e97841267df13661744820072fed7b39ff843a8d614575a6a8b430f7eae5c1bac4a22165997','admin','active','2026-01-09 17:33:18','female'),(2,'Siddhi Salokhe','siddhi@gmail.com','9604662020','scrypt:32768:8:1$7QYMdIK9H8Zd0o35$55e33396ad04a6e1a1ce6e5db4938854cb3a44bda19772f422b8cb0ecd1ee6256568fbef45d06ddcc7aab0933f6b998902c0c90bf41ddf80ea5157d0be66c346','student','active','2026-01-09 17:37:59','female'),(3,'Rahi Patil','rahi@gmail.com','8010917173','scrypt:32768:8:1$8XH0jVH2r1VWlyDr$6b7a88e5dbdb8d225dd9bea4c981073bfc480c9ff8bfffd51d45d1fef0c35e71d02722be91a081fce7632271483da451c49d97801b74e863454bb56bf05ee050','student','active','2026-01-09 17:38:59','female'),(4,'Arya Patil','arya@gmail.com','9403693787','scrypt:32768:8:1$WscQTnS3lPZaevNj$c7bac21ebc027b51d86c2e7405e3e01c0a49e413a6e3498ef9f500a4f6383c32242696769f84b02a77de922c915f62fef7aee1ca1c827cd6fcfaa553a19e16d7','provider','active','2026-01-09 17:40:11','female'),(5,'Arpita Patil','arpita@gmail.com','8483976939','scrypt:32768:8:1$g04VE68ufV6GDGoZ$7d29e17186888ab1ab70da6df56e3e2fd1e2528dc4a88e127b97d773fefbd4dab448666f6e67814eb81276d03ad300245ddb2664047e3a3f22ef627741c16370','provider','active','2026-01-09 17:40:54','female'),(6,'Siddhi Kasbekar','siddhi1@gmail.com','9322064260','scrypt:32768:8:1$pWYJQob0nWKyBQN7$ac7b23f7939d51d5c42b0be6184a24fb2e253ed68db9e057f3477587b9b1e85b7029e3f95d119e06eb7cacca53691a85da4e5c511cb22d074edc69c942aa196a','provider','active','2026-01-10 07:03:24','female'),(7,'Vaishnavi Patil','v@gmail.com','7821070219','scrypt:32768:8:1$Bt6tAOX9nAzzfGwD$79d8335469288ba9622f5708f8b8334a8c73f2d8db13faec214ac5ef80085b45e14b604a2c79d71d7bff5ab0aff4403fb7e403530f3b33ff0788ad40c1706552','student','active','2026-03-28 07:12:59','female'),(8,'Nita Salokhe','nita01@gmail.com','9096251022','scrypt:32768:8:1$F8auHFwAzOtF2F5G$5e7d9e928cea88a2bfa384c91149b229342d5f5b9cfd3dde34da3a7048243869a826ac92aa7384d039b3fb21ee446442c99a8c03a3c331300386c4b14a702788','student','active','2026-03-31 06:12:42','female');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-02 15:29:27
