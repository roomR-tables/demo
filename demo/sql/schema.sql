CREATE TABLE `settings` (
  `device_id` VARCHAR(30),
  `status` VARCHAR(30),
  `room_width` FLOAT,
  `room_height` FLOAT
);

CREATE TABLE `tables` (
  `id` INT,
  `x_pos` DECIMAL,
  `y_pos` DECIMAL
);

INSERT INTO `settings` VALUES ("0000000000000000", "available", 1000, 800);
INSERT INTO `tables` VALUES(1, 0, 0);