/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 80025
Source Host           : localhost:3306
Source Database       : mall

Target Server Type    : MYSQL
Target Server Version : 80025
File Encoding         : 65001

Date: 2021-06-06 08:08:04
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for account_tb
-- ----------------------------
DROP TABLE IF EXISTS `account_tb`;
CREATE TABLE `account_tb` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `account_name` varchar(255) NOT NULL COMMENT '用户名',
  `head_url` varchar(255) NOT NULL COMMENT '头像URL',
  `cell_phone` varchar(20) NOT NULL COMMENT '手机号',
  `addr` varchar(255) NOT NULL COMMENT '地址',
  `sex` tinyint NOT NULL COMMENT '性别（0：未知，1：男，2：女）',
  `birthday` date NOT NULL COMMENT '出生日期',
  `money` decimal(10,2) NOT NULL COMMENT '余额',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '最后修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_account_tb_account_name` (`account_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
