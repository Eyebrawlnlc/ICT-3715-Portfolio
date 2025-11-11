-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3307
-- Generation Time: Nov 11, 2025 at 06:29 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `amandla_locker_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `admin_id` int(11) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `booking_id` int(11) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `student_id` int(11) DEFAULT NULL,
  `locker_id` int(11) DEFAULT NULL,
  `booking_date` date DEFAULT NULL,
  `payment_status` enum('Paid','Unpaid') DEFAULT 'Unpaid'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`booking_id`, `parent_id`, `student_id`, `locker_id`, `booking_date`, `payment_status`) VALUES
(1, 1, 1, 1, '2025-11-01', 'Unpaid'),
(2, 2, 2, 2, '2025-11-01', 'Unpaid'),
(3, 3, 3, 3, '2025-11-01', 'Unpaid'),
(4, 4, 4, 4, '2025-11-01', 'Unpaid'),
(5, 5, 5, 5, '2025-11-01', 'Unpaid'),
(6, 6, 6, 6, '2025-11-01', 'Unpaid'),
(7, 7, 7, 7, '2025-11-01', 'Unpaid'),
(8, 8, 8, 8, '2025-11-01', 'Unpaid'),
(9, 9, 9, 9, '2025-11-01', 'Unpaid'),
(10, 10, 10, 10, '2025-11-01', 'Unpaid'),
(11, 11, 11, 11, '2025-11-01', 'Unpaid'),
(12, 12, 12, 12, '2025-11-01', 'Unpaid'),
(13, 13, 13, 13, '2025-11-01', 'Unpaid'),
(14, 14, 14, 14, '2025-11-01', 'Unpaid'),
(15, 15, 15, 15, '2025-11-01', 'Unpaid'),
(16, 16, 16, 16, '2025-11-01', 'Unpaid'),
(17, 17, 17, 17, '2025-11-01', 'Unpaid'),
(18, 18, 18, 18, '2025-11-01', 'Unpaid'),
(19, 19, 19, 19, '2025-11-01', 'Unpaid'),
(20, 20, 20, 20, '2025-11-01', 'Unpaid'),
(21, 21, 21, 21, '2025-11-01', 'Unpaid'),
(22, 22, 22, 22, '2025-11-01', 'Unpaid'),
(23, 23, 23, 23, '2025-11-01', 'Unpaid'),
(24, 24, 24, 24, '2025-11-01', 'Unpaid'),
(25, 25, 25, 25, '2025-11-01', 'Unpaid'),
(26, 26, 26, 26, '2025-11-01', 'Unpaid'),
(27, 27, 27, 27, '2025-11-01', 'Unpaid'),
(28, 28, 28, 28, '2025-11-01', 'Unpaid'),
(29, 29, 29, 29, '2025-11-01', 'Unpaid'),
(30, 30, 30, 30, '2025-11-01', 'Unpaid');

-- --------------------------------------------------------

--
-- Table structure for table `lockers`
--

CREATE TABLE `lockers` (
  `locker_id` int(11) NOT NULL,
  `locker_number` varchar(10) DEFAULT NULL,
  `status` enum('Available','Booked','Suspended') DEFAULT 'Available',
  `location` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `lockers`
--

INSERT INTO `lockers` (`locker_id`, `locker_number`, `status`, `location`) VALUES
(1, '101', 'Available', 'Main Hall'),
(2, '102', 'Available', 'Main Hall'),
(3, '103', 'Available', 'Main Hall'),
(4, '104', 'Available', 'Main Hall'),
(5, '105', 'Available', 'Main Hall'),
(6, '106', 'Available', 'Main Hall'),
(7, '107', 'Available', 'Main Hall'),
(8, '108', 'Available', 'Main Hall'),
(9, '109', 'Available', 'Main Hall'),
(10, '110', 'Available', 'Main Hall'),
(11, '111', 'Available', 'Main Hall'),
(12, '112', 'Available', 'Main Hall'),
(13, '113', 'Available', 'Main Hall'),
(14, '114', 'Available', 'Main Hall'),
(15, '115', 'Available', 'Main Hall'),
(16, '116', 'Available', 'Main Hall'),
(17, '117', 'Available', 'Main Hall'),
(18, '118', 'Available', 'Main Hall'),
(19, '119', 'Available', 'Main Hall'),
(20, '120', 'Available', 'Main Hall'),
(21, '121', 'Available', 'Main Hall'),
(22, '122', 'Available', 'Main Hall'),
(23, '123', 'Available', 'Main Hall'),
(24, '124', 'Available', 'Main Hall'),
(25, '125', 'Available', 'Main Hall'),
(26, '126', 'Available', 'Main Hall'),
(27, '127', 'Available', 'Main Hall'),
(28, '128', 'Available', 'Main Hall'),
(29, '129', 'Available', 'Main Hall'),
(30, '130', 'Available', 'Main Hall'),
(31, '131', 'Available', 'Main Hall'),
(32, '132', 'Available', 'Main Hall'),
(33, '133', 'Available', 'Main Hall'),
(34, '134', 'Available', 'Main Hall'),
(35, '135', 'Available', 'Main Hall'),
(36, '136', 'Available', 'Main Hall'),
(37, '137', 'Available', 'Main Hall'),
(38, '138', 'Available', 'Main Hall'),
(39, '139', 'Available', 'Main Hall'),
(40, '140', 'Available', 'Main Hall'),
(41, '141', 'Available', 'Main Hall'),
(42, '142', 'Available', 'Main Hall'),
(43, '143', 'Available', 'Main Hall'),
(44, '144', 'Available', 'Main Hall'),
(45, '145', 'Available', 'Main Hall'),
(46, '146', 'Available', 'Main Hall'),
(47, '147', 'Available', 'Main Hall'),
(48, '148', 'Available', 'Main Hall'),
(49, '149', 'Available', 'Main Hall'),
(50, '150', 'Available', 'Main Hall'),
(51, '151', 'Available', 'Main Hall'),
(52, '152', 'Available', 'Main Hall'),
(53, '153', 'Available', 'Main Hall'),
(54, '154', 'Available', 'Main Hall'),
(55, '155', 'Available', 'Main Hall'),
(56, '156', 'Available', 'Main Hall'),
(57, '157', 'Available', 'Main Hall'),
(58, '158', 'Available', 'Main Hall'),
(59, '159', 'Available', 'Main Hall'),
(60, '160', 'Available', 'Main Hall');

-- --------------------------------------------------------

--
-- Table structure for table `parents`
--

CREATE TABLE `parents` (
  `parent_id` int(11) NOT NULL,
  `title` varchar(10) DEFAULT NULL,
  `id_number` varchar(20) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `parents`
--

INSERT INTO `parents` (`parent_id`, `title`, `id_number`, `first_name`, `last_name`, `email`, `address`, `phone_number`) VALUES
(1, 'Mrs', '3018701182', 'Mary', 'Johnson', 'mary.j@gmail.com', '456 Oak Ave', '832345678'),
(2, 'Ms', '9504200125035', 'Linda', 'Brown', 'linda.brown@gmail.com', '789 Pine Rd', '843456789'),
(3, 'Mr', '9411277787016', 'David', 'Johnson', 'david.johnson@gmail.com', '321 Maple Lane', '745678901'),
(4, 'Mrs', '9298654199', 'Emma', 'Wilson', 'emma.wilson@gmail.com', '654 Cedar Drive', '756789012'),
(5, 'Dr', '9212011817041', 'Robert', 'Taylor', 'robert.taylor@gmail.com', '987 Birch Boulevard', '767890123'),
(6, 'Ms', '5004038523192', 'Linda', 'Anderson', 'linda.anderson@gmail.com', '135 Spruce Street', '778901234'),
(7, 'Mr', '4109137427178', 'James', 'Thomas', 'james.thomas@gmail.com', '246 Redwood Court', '789012345'),
(8, 'Mrs', '5612226663035', 'Robert', 'Wilson', 'robert.wilson@gmail.com', '189 Pine Street', '735460310'),
(9, 'Mr', '910173547175', 'Michael', 'Anderson', 'michael.anderson@gmail.com', '702 Maple Street', '775510858'),
(10, 'Ms', '4207012946087', 'Emma', 'Smith', 'emma.smith@gmail.com', '718 Ash Street', '749100605'),
(11, 'Mrs', '8305068147131', 'Ava', 'Smith', 'ava.smith@gmail.com', '599 Spruce Street', '783072551'),
(12, 'Mr', '9505017498148', 'Ava', 'Hall', 'ava.hall@gmail.com', '332 Maple Street', '791798774'),
(13, 'Ms', '6602050571067', 'Liam', 'White', 'liam.white@gmail.com', '842 Birch Street', '737988829'),
(14, 'Mrs', '9012129123195', 'Noah', 'Hall', 'noah.hall@gmail.com', '190 Willow Street', '743682129'),
(15, 'Dr', '306052541142', 'Emma', 'Anderson', 'emma.anderson@gmail.com', '704 Willow Street', '721206388'),
(16, 'Ms', '9507203452020', 'Robert', 'Anderson', 'robert.anderson@gmail.com', '875 Maple Street', '739094911'),
(17, 'Mr', '6806020888197', 'Michael', 'Nkosi', 'michael.nkosi@gmail.com', '897 Cedar Street', '798801632'),
(18, 'Dr', '7807275046086', 'Liam', 'Brown', 'liam.brown@gmail.com', '492 Spruce Street', '786828544'),
(19, 'Dr', '4809209872196', 'Robert', 'Smith', 'robert.smith@gmail.com', '757 Cedar Street', '768346836'),
(20, 'Mrs', '4204287904104', 'Liam', 'Nkosi', 'liam.nkosi@gmail.com', '433 Birch Street', '744083306'),
(21, 'Mr', '5707284141112', 'Liam', 'Anderson', 'liam.anderson@gmail.com', '327 Redwood Street', '796115093'),
(22, 'Mr', '7009119979038', 'Ava', 'Wilson', 'ava.wilson@gmail.com', '911 Birch Street', '764281373'),
(23, 'Dr', '4510283636054', 'Noah', 'White', 'noah.white@gmail.com', '604 Pine Street', '777393801'),
(24, 'Ms', '8502022675077', 'Jane', 'Anderson', 'jane.anderson@gmail.com', '431 Spruce Street', '758356276'),
(25, 'Ms', '6305123394192', 'Emma', 'Johnson', 'emma.johnson@gmail.com', '715 Birch Street', '763177499'),
(26, 'Mr', '5912127358130', 'Michael', 'White', 'michael.white@gmail.com', '238 Oak Street', '743043868'),
(27, 'Mrs', '6603287420165', 'Sophia', 'Hall', 'sophia.hall@gmail.com', '776 Cedar Street', '778621486'),
(28, 'Mr', '6012217265129', 'John', 'Nkosi', 'john.nkosi@gmail.com', '600 Elm Street', '728680821'),
(29, 'Ms', '9602046538016', 'Ava', 'Thomas', 'ava.thomas@gmail.com', '446 Redwood Street', '711846135'),
(30, 'Dr', '7303154126003', 'Ethan', 'Taylor', 'ethan.taylor@gmail.com', '404 Oak Street', '799314784'),
(31, 'Ms', '202019503196', 'Jane', 'Taylor', 'jane.taylor@gmail.com', '911 Ash Street', '781998910'),
(32, 'Mrs', '5512102556093', 'Liam', 'Wilson', 'liam.wilson@gmail.com', '413 Ash Street', '748585981'),
(33, 'Mr', '9309202925129', 'Liam', 'Smith', 'liam.smith@gmail.com', '310 Maple Street', '742749180'),
(34, 'Mrs', '809035978098', 'John', 'Smith', 'john.smith@gmail.com', '140 Maple Street', '775223322'),
(35, 'Ms', '9912089374198', 'Sophia', 'Hall', 'sophia.hall@gmail.com', '661 Maple Street', '777667807'),
(36, 'Mr', '1008113111123', 'Ethan', 'Wilson', 'ethan.wilson@gmail.com', '636 Cedar Street', '737248373'),
(37, 'Mr', '912266784015', 'Noah', 'Nkosi', 'noah.nkosi@gmail.com', '353 Oak Street', '763407066'),
(38, 'Mr', '6711189204048', 'Ethan', 'Nkosi', 'ethan.nkosi@gmail.com', '382 Elm Street', '738510987'),
(39, 'Mrs', '6301209154077', 'Olivia', 'Hall', 'olivia.hall@gmail.com', '864 Cedar Street', '717403055'),
(40, 'Mrs', '7811225151184', 'Emma', 'Johnson', 'emma.johnson@gmail.com', '483 Oak Street', '787978403'),
(41, 'Dr', '4608148192183', 'John', 'Anderson', 'john.anderson@gmail.com', '789 Willow Street', '777769694'),
(42, 'Mr', '6204032653193', 'Michael', 'Taylor', 'michael.taylor@gmail.com', '701 Spruce Street', '721216884'),
(43, 'Dr', '4901218928125', 'Michael', 'Thomas', 'michael.thomas@gmail.com', '104 Elm Street', '711790361'),
(44, 'Mrs', '5206163043195', 'David', 'Taylor', 'david.taylor@gmail.com', '744 Maple Street', '749909129'),
(45, 'Ms', '9108286769008', 'Noah', 'Taylor', 'noah.taylor@gmail.com', '566 Ash Street', '787273081'),
(46, 'Mr', '4609139102037', 'Olivia', 'Smith', 'olivia.smith@gmail.com', '216 Oak Street', '763380717'),
(47, 'Ms', '6104301288034', 'Emily', 'Brown', 'emily.brown@gmail.com', '906', '719919743'),
(48, 'Dr', '8612145459128', 'Robert', 'Anderson', 'robert.anderson@gmail.com', '991 Redwood Street', '764100813'),
(49, 'Mr', '4108192658003', 'Olivia', 'Anderson', 'olivia.anderson@gmail.com', '404 Cedar Street', '714962168');

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `student_id` int(11) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `grade` varchar(20) DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`student_id`, `first_name`, `last_name`, `grade`, `parent_id`) VALUES
(1, 'Liam', 'Johnson', 'Grade 8', 1),
(2, 'Olivia', 'Brown', 'Grade 10', 2),
(3, 'Liam', 'Johnson', 'Grade 10', 3),
(4, 'Olivia', 'Wilson', 'Grade 9', 4),
(5, 'Noah', 'Taylor', 'Grade 8', 5),
(6, 'Ava', 'Anderson', 'Grade 11', 6),
(7, 'Ethan', 'Thomas', 'Grade 10', 7),
(8, 'James', 'Wilson', 'Grade 9', 8),
(9, 'Noah', 'Anderson', 'Grade 9', 9),
(10, 'Liam', 'Smith', 'Grade 10', 10),
(11, 'Ava', 'Smith', 'Grade 10', 11),
(12, 'Emily', 'Hall', 'Grade 1', 12),
(13, 'Jane', 'White', 'Grade 8', 13),
(14, 'John', 'Hall', 'Grade 10', 14),
(15, 'Jane', 'Anderson', 'Grade 11', 15),
(16, 'Michael', 'Anderson', 'Grade 9', 16),
(17, 'David', 'Nkosi', 'Grade 8', 17),
(18, 'Emily', 'Brown', 'Grade 10', 18),
(19, 'Alice', 'Smith', 'Grade 8', 19),
(20, 'Jane', 'Nkosi', 'Grade 10', 20),
(21, 'Emily', 'Anderson', 'Grade 9', 21),
(22, 'Michael', 'Wilson', 'Grade 10', 22),
(23, 'Ava', 'White', 'Grade 11', 23),
(24, 'Ethan', 'Anderson', 'Grade 8', 24),
(25, 'Alice', 'Johnson', 'Grade 11', 25),
(26, 'Robert', 'White', 'Grade 9', 26),
(27, 'Liam', 'Hall', 'Grade 8', 27),
(28, 'Liam', 'Nkosi', 'Grade 8', 28),
(29, 'Robert', 'Thomas', 'Grade 8', 29),
(30, 'Olivia', 'Taylor', 'Grade 8', 30),
(31, 'Alice', 'Taylor', 'Grade 9', 31),
(32, 'Ethan', 'Wilson', 'Grade 12', 32),
(33, 'Ethan', 'Smith', 'Grade 10', 33),
(34, 'Emma', 'Smith', 'Grade 10', 34),
(35, 'John', 'Hall', 'Grade 8', 35),
(36, 'Alice', 'Wilson', 'Grade 12', 36),
(37, 'Olivia', 'Nkosi', 'Grade 10', 37),
(38, 'Liam', 'Nkosi', 'Grade 10', 38),
(39, 'James', 'Hall', 'Grade 8', 39),
(40, 'Olivia', 'Johnson', 'Grade 9', 40),
(41, 'James', 'Anderson', 'Grade 11', 41),
(42, 'John', 'Taylor', 'Grade 11', 42),
(43, 'Sophia', 'Thomas', 'Grade 9', 43),
(44, 'Ava', 'Taylor', 'Grade 11', 44),
(45, 'Sophia', 'Taylor', 'Grade 8', 45),
(46, 'Olivia', 'Smith', 'Grade 12', 46),
(47, 'James', 'Brown', 'Grade 10', 47),
(48, 'Ava', 'Anderson', 'Grade 11', 48),
(49, 'Liam', 'Anderson', 'Grade 9', 49);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`admin_id`);

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`booking_id`),
  ADD KEY `parent_id` (`parent_id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `locker_id` (`locker_id`);

--
-- Indexes for table `lockers`
--
ALTER TABLE `lockers`
  ADD PRIMARY KEY (`locker_id`),
  ADD UNIQUE KEY `locker_number` (`locker_number`);

--
-- Indexes for table `parents`
--
ALTER TABLE `parents`
  ADD PRIMARY KEY (`parent_id`),
  ADD UNIQUE KEY `id_number` (`id_number`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`student_id`),
  ADD KEY `parent_id` (`parent_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `booking_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `lockers`
--
ALTER TABLE `lockers`
  MODIFY `locker_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT for table `parents`
--
ALTER TABLE `parents`
  MODIFY `parent_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=402;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `student_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=226;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `parents` (`parent_id`),
  ADD CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`),
  ADD CONSTRAINT `bookings_ibfk_3` FOREIGN KEY (`locker_id`) REFERENCES `lockers` (`locker_id`);

--
-- Constraints for table `students`
--
ALTER TABLE `students`
  ADD CONSTRAINT `students_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `parents` (`parent_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- =============================================
-- MIS REPORTS SECTION
-- =============================================

-- REPORT 1: Locker Usage by Grade Report
SELECT 
    s.grade AS Grade,
    COUNT(b.booking_id) AS LockersBooked,
    (
        SELECT COUNT(*) 
        FROM lockers l
    ) AS TotalLockers,
    ROUND(
        (COUNT(b.booking_id) * 100.0 / (SELECT COUNT(*) FROM lockers l)),
        2
    ) AS PercentageUsed
FROM 
    bookings b
JOIN 
    students s ON b.student_id = s.student_id
WHERE 
    s.grade IN ('Grade 8', 'Grade 11')
    AND b.payment_status = 'Paid'
GROUP BY 
    s.grade;

-- REPORT 2: Locker Booking Summary (Jan–Jun 2026)
SELECT 
    COUNT(*) AS TotalLockersBooked
FROM 
    bookings
WHERE 
    booking_date BETWEEN '2026-01-01' AND '2026-06-30'
    AND payment_status = 'Paid';
