DROP TABLE IF EXISTS `rxnconso`;
CREATE TABLE `rxnconso` (
  `RXCUI` varchar(8) NOT NULL,
  `LAT` varchar(3) NOT NULL DEFAULT 'ENG',
  `TS` varchar(1) DEFAULT NULL,
  `LUI` varchar(8) DEFAULT NULL,
  `STT` varchar(3) DEFAULT NULL,
  `SUI` varchar(8) DEFAULT NULL,
  `ISPREF` varchar(1) DEFAULT NULL,
  `RXAUI` varchar(8) NOT NULL,
  `SAUI` varchar(50) DEFAULT NULL,
  `SCUI` varchar(50) DEFAULT NULL,
  `SDUI` varchar(50) DEFAULT NULL,
  `SAB` varchar(20) NOT NULL,
  `TTY` varchar(20) NOT NULL,
  `CODE` varchar(50) NOT NULL,
  `STR` varchar(3000) NOT NULL,
  `SRL` varchar(10) DEFAULT NULL,
  `SUPPRESS` varchar(1) DEFAULT NULL,
  `CVF` varchar(50) DEFAULT NULL,
  `CONCAT_B4_SAUI` varchar(40) GENERATED ALWAYS AS (concat(coalesce(`RXCUI`,_utf8mb4''),coalesce(`LAT`,_utf8mb4''),coalesce(`TS`,_utf8mb4''),coalesce(`LUI`,_utf8mb4''),coalesce(`STT`,_utf8mb4''),coalesce(`SUI`,_utf8mb4''),coalesce(`ISPREF`,_utf8mb4''),coalesce(`RXAUI`,_utf8mb4''))) STORED,
  `STR_MD5` char(32) DEFAULT NULL,
  `create_file_date` date DEFAULT NULL,
  `last_update_file_date` date DEFAULT NULL,
  PRIMARY KEY (`RXAUI`),
  UNIQUE KEY `uk_rxnconso` (`CONCAT_B4_SAUI`,`SCUI`,`SDUI`,`SAB`,`TTY`,`CODE`,`STR_MD5`,`STR`(50),`SRL`,`SUPPRESS`,`CVF`) /*!80000 INVISIBLE */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `rxncuichanges`;
CREATE TABLE `rxncuichanges` (
  `RXAUI` varchar(8) DEFAULT NULL,
  `CODE` varchar(50) DEFAULT NULL,
  `SAB` varchar(20) DEFAULT NULL,
  `TTY` varchar(20) DEFAULT NULL,
  `STR` varchar(3000) DEFAULT NULL,
  `OLD_RXCUI` varchar(8) NOT NULL,
  `NEW_RXCUI` varchar(8) NOT NULL,
  `STR_MD5` char(32) DEFAULT NULL,
  `create_file_date` date DEFAULT NULL,
  `last_update_file_date` date DEFAULT NULL,
  UNIQUE KEY `uk_rxncuichanges` (`RXAUI`,`CODE`,`SAB`,`TTY`,`OLD_RXCUI`,`NEW_RXCUI`,`STR_MD5`,`STR`(50))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `rxnrel`;
CREATE TABLE `rxnrel` (
  `RXCUI1` varchar(8) DEFAULT NULL,
  `RXAUI1` varchar(8) DEFAULT NULL,
  `STYPE1` varchar(50) DEFAULT NULL,
  `REL` varchar(4) DEFAULT NULL,
  `RXCUI2` varchar(8) DEFAULT NULL,
  `RXAUI2` varchar(8) DEFAULT NULL,
  `STYPE2` varchar(50) DEFAULT NULL,
  `RELA` varchar(100) DEFAULT NULL,
  `RUI` varchar(10) DEFAULT NULL,
  `SRUI` varchar(50) DEFAULT NULL,
  `SAB` varchar(20) NOT NULL,
  `SL` varchar(1000) DEFAULT NULL,
  `DIR` varchar(1) DEFAULT NULL,
  `RG` varchar(10) DEFAULT NULL,
  `SUPPRESS` varchar(1) DEFAULT NULL,
  `CVF` varchar(50) DEFAULT NULL,
  `SL_MD5` char(32) DEFAULT NULL,
  `create_file_date` date DEFAULT NULL,
  `last_update_file_date` date DEFAULT NULL,
  UNIQUE KEY `uk_rxnrel` (`RXAUI1`,`RXCUI1`,`RXAUI2`,`RXCUI2`,`REL`,`RUI`,`RELA`,`STYPE1`,`STYPE2`,`SRUI`,`SAB`,`DIR`,`RG`,`SUPPRESS`,`CVF`,`SL_MD5`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `rxnsat`;
CREATE TABLE `rxnsat` (
  `RXCUI` varchar(8) DEFAULT NULL,
  `LUI` varchar(8) DEFAULT NULL,
  `SUI` varchar(8) DEFAULT NULL,
  `RXAUI` varchar(9) DEFAULT NULL,
  `STYPE` varchar(50) DEFAULT NULL,
  `CODE` varchar(50) DEFAULT NULL,
  `ATUI` varchar(11) DEFAULT NULL,
  `SATUI` varchar(50) DEFAULT NULL,
  `ATN` varchar(1000) NOT NULL,
  `SAB` varchar(20) NOT NULL,
  `ATV` varchar(4000) DEFAULT NULL,
  `SUPPRESS` varchar(1) DEFAULT NULL,
  `CVF` varchar(50) DEFAULT NULL,
  `ATN_MD5` char(32) DEFAULT NULL,
  `ATV_MD5` char(32) DEFAULT NULL,
  `create_file_date` date DEFAULT NULL,
  `last_update_file_date` date DEFAULT NULL,
  UNIQUE KEY `uk_rxnsat` (`RXAUI`,`RXCUI`,`SAB`,`ATN_MD5`,`ATV_MD5`,`ATN`(50),`ATV`(50),`LUI`,`SUI`,`STYPE`,`CODE`,`ATUI`,`SATUI`,`SUPPRESS`,`CVF`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `rxnsty`;
CREATE TABLE `rxnsty` (
  `RXCUI` varchar(8) NOT NULL,
  `TUI` varchar(4) DEFAULT NULL,
  `STN` varchar(100) DEFAULT NULL,
  `STY` varchar(50) DEFAULT NULL,
  `ATUI` varchar(11) DEFAULT NULL,
  `CVF` varchar(50) DEFAULT NULL,
  `create_file_date` date DEFAULT NULL,
  `last_update_file_date` date DEFAULT NULL,
  UNIQUE KEY `uk_rxnsty` (`RXCUI`,`STY`,`TUI`,`STN`,`ATUI`,`CVF`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;