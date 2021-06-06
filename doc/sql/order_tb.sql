/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 80025
Source Host           : localhost:3306
Source Database       : mall

Target Server Type    : MYSQL
Target Server Version : 80025
File Encoding         : 65001

Date: 2021-06-06 08:08:16
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for order_tb
-- ----------------------------
DROP TABLE IF EXISTS `order_tb`;
CREATE TABLE `order_tb` (
  `id` int NOT NULL COMMENT '主键',
  `account_id` int NOT NULL COMMENT '账户id',
  `commodity_id` int NOT NULL COMMENT '商品id',
  `number` int NOT NULL COMMENT '商品数量',
  `order_amount` decimal(10,2) NOT NULL COMMENT '订单总金额',
  `addr` varchar(255) NOT NULL COMMENT '收货地址',
  `order_status` tinyint NOT NULL COMMENT '订单状态（0：未支付，1：已支付，2：换货，3：退货）',
  `creat_time` datetime NOT NULL COMMENT '订单创建时间',
  `payment_time` datetime DEFAULT NULL COMMENT '订单付款时间',
  `close_time` datetime DEFAULT NULL COMMENT '订单成交时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
