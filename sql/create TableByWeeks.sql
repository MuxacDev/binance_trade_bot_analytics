use TradeBotDb;
CREATE TABLE `TableByWeeks` (
  `id` varchar(70) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `sel_interval` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `period` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `step` SMALLINT NULL,
  `vol_btc` double(20,5),
  `vol_usd` double(17,2),
  `bal_btc` double(20,5),
  `bal_usd` double(17,2),
  `old_ord` SMALLINT NULL,
  `max_usage` varchar(5) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `margin` double(4,3) NULL,
  `per` varchar(5) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `current_price` double(17,2),
  `start_sum` double(17,2),
  `total_sum` double(17,2),
  `bal_margin` double(6,2),
  `duration` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `comb_status` varchar(15) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;