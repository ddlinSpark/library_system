/*
 Navicat Premium Dump SQL

 Source Server         : 云服务器
 Source Server Type    : MySQL
 Source Server Version : 50728 (5.7.28)
 Source Host           : 8.155.21.3:3306
 Source Schema         : library

 Target Server Type    : MySQL
 Target Server Version : 50728 (5.7.28)
 File Encoding         : 65001

 Date: 26/12/2024 13:03:54
*/

-- ----------------------------
-- This section is reserved for future SQL commands or comments.
-- ----------------------------
DROP DATABASE IF EXISTS library;
CREATE DATABASE IF NOT EXISTS library CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE library;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for books
-- ----------------------------
DROP TABLE IF EXISTS `books`;
CREATE TABLE `books`  (
  `book_id` int(11) NULL DEFAULT NULL,
  `isbn` varchar(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `author` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `publisher` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `publish_date` date NULL DEFAULT NULL,
  `category` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `location` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `price` decimal(10, 2) NULL DEFAULT NULL,
  `total_copies` int(11) NULL DEFAULT NULL,
  `available_copies` int(11) NULL DEFAULT NULL,
  `status` enum('available','borrowed') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of books
-- ----------------------------
INSERT INTO `books` VALUES (1, '9787123456788', '测试书1', '测试人员1', '测试人员1', '2022-02-02', '计算机', 'A区-01-01', 0.00, 1, -1, 'available', NULL, '2024-12-26 00:39:24', '2024-12-26 01:37:43');
INSERT INTO `books` VALUES (2, '9787123456788', '测试数2', '测试人员2', '测试人员2', '2020-02-02', '计算机', 'A区-01-02', 0.00, 1, 1, 'available', NULL, '2024-12-26 00:39:24', '2024-12-26 01:32:17');

-- ----------------------------
-- Table structure for borrowing_records
-- ----------------------------
DROP TABLE IF EXISTS `borrowing_records`;
CREATE TABLE `borrowing_records`  (
  `record_id` int(11) NULL DEFAULT NULL,
  `user_id` int(11) NULL DEFAULT NULL,
  `book_id` int(11) NULL DEFAULT NULL,
  `borrow_date` timestamp NULL DEFAULT NULL,
  `due_date` timestamp NULL DEFAULT NULL,
  `return_date` timestamp NULL DEFAULT NULL,
  `status` enum('borrowed','returned','overdue','lost') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `fine_amount` decimal(10, 2) NULL DEFAULT NULL,
  `fine_paid` tinyint(1) NULL DEFAULT NULL,
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `renew_count` int(11) NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of borrowing_records
-- ----------------------------
INSERT INTO `borrowing_records` VALUES (1, 2, 2, '2024-12-26 00:00:00', '2025-01-25 00:00:00', '2024-12-26 00:00:00', 'returned', 0.00, 0, NULL, 0);
INSERT INTO `borrowing_records` VALUES (2, 2, 1, '2024-12-26 00:00:00', '2025-01-25 00:00:00', NULL, 'borrowed', 0.00, 0, NULL, 0);

-- ----------------------------
-- Table structure for reservations
-- ----------------------------
DROP TABLE IF EXISTS `reservations`;
CREATE TABLE `reservations`  (
  `reservation_id` int(11) NULL DEFAULT NULL,
  `user_id` int(11) NULL DEFAULT NULL,
  `book_id` int(11) NULL DEFAULT NULL,
  `reserve_date` timestamp NULL DEFAULT NULL,
  `status` enum('waiting','completed','cancelled') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of reservations
-- ----------------------------

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `user_id` int(11) NULL DEFAULT NULL,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `role` enum('admin','user') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `real_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `last_login` timestamp NULL DEFAULT NULL,
  `status` tinyint(1) NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'admin', '123456', 'admin', '系统管理员', NULL, NULL, '2024-12-26 00:39:24', '2024-12-26 02:10:38', 1);
INSERT INTO `users` VALUES (2, 'test_user', '123456', 'user', '测试用户', '13800138000', 'test@example.com', '2024-12-26 00:39:24', '2024-12-26 02:03:19', 1);

SET FOREIGN_KEY_CHECKS = 1;
