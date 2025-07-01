-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: cinedream
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-06-28 07:06:38.938289'),(2,'auth','0001_initial','2025-06-28 07:06:40.441352'),(3,'admin','0001_initial','2025-06-28 07:06:40.770115'),(4,'admin','0002_logentry_remove_auto_add','2025-06-28 07:06:40.786657'),(5,'admin','0003_logentry_add_action_flag_choices','2025-06-28 07:06:40.800554'),(6,'contenttypes','0002_remove_content_type_name','2025-06-28 07:06:41.064107'),(7,'auth','0002_alter_permission_name_max_length','2025-06-28 07:06:41.210279'),(8,'auth','0003_alter_user_email_max_length','2025-06-28 07:06:41.258250'),(9,'auth','0004_alter_user_username_opts','2025-06-28 07:06:41.272969'),(10,'auth','0005_alter_user_last_login_null','2025-06-28 07:06:41.431301'),(11,'auth','0006_require_contenttypes_0002','2025-06-28 07:06:41.440275'),(12,'auth','0007_alter_validators_add_error_messages','2025-06-28 07:06:41.458006'),(13,'auth','0008_alter_user_username_max_length','2025-06-28 07:06:41.606422'),(14,'auth','0009_alter_user_last_name_max_length','2025-06-28 07:06:41.758444'),(15,'auth','0010_alter_group_name_max_length','2025-06-28 07:06:41.793206'),(16,'auth','0011_update_proxy_permissions','2025-06-28 07:06:41.810411'),(17,'auth','0012_alter_user_first_name_max_length','2025-06-28 07:06:41.983466'),(18,'sessions','0001_initial','2025-06-28 07:06:42.077262'),(19,'movies','0001_initial','2025-06-29 05:52:42.003883'),(20,'users','0001_initial','2025-06-29 06:56:53.909922'),(21,'cinema','0001_initial','2025-06-29 06:56:53.964517'),(22,'room','0001_initial','2025-06-29 06:56:54.325711'),(23,'seats','0001_initial','2025-06-29 06:56:54.564567'),(24,'movies','0002_remove_movie_duration_remove_movie_rating_and_more','2025-06-29 06:56:55.250563'),(25,'schedule','0001_initial','2025-06-29 06:56:55.683647'),(26,'booking','0001_initial','2025-06-29 06:56:56.187665'),(27,'cinema','0002_alter_cinema_options','2025-07-01 01:16:16.125797'),(28,'cinema','0003_alter_cinema_table','2025-07-01 01:16:16.163417'),(29,'movies','0003_alter_movie_options','2025-07-01 01:16:16.176033'),(30,'movies','0004_alter_movie_table','2025-07-01 01:16:16.191349'),(31,'room','0002_alter_room_options','2025-07-01 01:16:16.205268'),(32,'room','0003_alter_room_table','2025-07-01 01:16:16.219393');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-01 10:22:50
