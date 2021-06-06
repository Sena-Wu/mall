/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 80025
Source Host           : localhost:3306
Source Database       : mall

Target Server Type    : MYSQL
Target Server Version : 80025
File Encoding         : 65001

Date: 2021-06-06 07:42:24
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for commodity_tb
-- ----------------------------
DROP TABLE IF EXISTS `commodity_tb`;
CREATE TABLE `commodity_tb` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `price` decimal(10,2) NOT NULL COMMENT '商品单价',
  `description` varchar(200) NOT NULL COMMENT '商品描述',
  `total_stock` int NOT NULL COMMENT '总库存',
  `available_stock` int NOT NULL COMMENT '剩余库存',
  `create_time` datetime NOT NULL COMMENT '创建时间/上架时间',
  `update_time` datetime NOT NULL COMMENT '最后修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
