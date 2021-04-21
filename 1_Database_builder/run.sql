CREATE TABLE `AppUsers` (
  `uid` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `Taskperday` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `Follower` (
  `ID` int(11) NOT NULL,
  `Followed` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `Follower` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `DateUpdate` date NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `Following` (
  `ID` int(11) NOT NULL,
  `Follower` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `Followed` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `DateUpdate` date NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `HashtagAccount` (
  `ID` int(11) NOT NULL,
  `Account` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `Hashtag` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `Date` date NOT NULL,
  `numpost` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `Likes` (
  `ID` int(11) NOT NULL,
  `Liked` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `Liker` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `NumPosts` int(11) NOT NULL,
  `NumLiked` int(11) NOT NULL,
  `DateUpdate` date DEFAULT NULL,
  `Scrapped` tinyint(4) NOT NULL DEFAULT '0',
  `Publicornot` tinyint(4) DEFAULT NULL,
  `Followers` int(11) DEFAULT NULL,
  `Following` int(11) DEFAULT NULL,
  `Posts` int(11) DEFAULT NULL,
  `DateFailed` date DEFAULT NULL,
  `FailedTimes` int(11) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `LoyalFollowers` (
  `ID` int(11) NOT NULL,
  `Account` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `Follower` varchar(45) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `PremiumFollowedHistory` (
  `ID` int(11) NOT NULL,
  `Account` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `AccountFollowed` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `DateFollowed` date NOT NULL,
  `LikedOrNot` tinyint(4) DEFAULT NULL,
  `FollowedOrNot` int(11) DEFAULT NULL,
  `UnfollowedOrnot` int(11) DEFAULT NULL,
  `Scrapped` tinyint(4) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `PremiumTasks` (
  `idPremiumTasks` int(11) NOT NULL,
  `User` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `Task` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `Date` date NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `publicprofiles` (
  `username` varchar(50) NOT NULL,
  `Verified` tinyint(1) NOT NULL,
  `Posts` int(11) NOT NULL,
  `Followers` bigint(20) NOT NULL,
  `Following` int(11) DEFAULT NULL,
  `Bio` varchar(500) DEFAULT NULL,
  `Scrapped` tinyint(1) NOT NULL,
  `DataUpdated` date DEFAULT NULL,
  `BotScraping` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `BioCleaned` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ProfileLanguage` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `Taskbank` (
  `id` int(11) NOT NULL,
  `uid` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `Account` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `Task` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `TargetAccount` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Likepercentage` float DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `toscrape` (
  `username` varchar(50) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Account''s Which should be scrapped';


--
-- Indexes for table `AppUsers`
--
ALTER TABLE `AppUsers`
  ADD PRIMARY KEY (`uid`);

--
-- Indexes for table `Follower`
--
ALTER TABLE `Follower`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `Following`
--
ALTER TABLE `Following`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `HashtagAccount`
--
ALTER TABLE `HashtagAccount`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `Likes`
--
ALTER TABLE `Likes`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Likednames` (`Scrapped`);

--
-- Indexes for table `LoyalFollowers`
--
ALTER TABLE `LoyalFollowers`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `PremiumFollowedHistory`
--
ALTER TABLE `PremiumFollowedHistory`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `PremiumTasks`
--
ALTER TABLE `PremiumTasks`
  ADD PRIMARY KEY (`idPremiumTasks`);

--
-- Indexes for table `publicprofiles`
--
ALTER TABLE `publicprofiles`
  ADD PRIMARY KEY (`username`),
  ADD KEY `usernameindex` (`username`);

--
-- Indexes for table `SpecialAccount`
--
ALTER TABLE `SpecialAccount`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `TargetAccounts`
--
ALTER TABLE `TargetAccounts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Taskbank`
--
ALTER TABLE `Taskbank`
  ADD PRIMARY KEY (`id`),
  ADD KEY `accountnames` (`Account`);

--
-- Indexes for table `Tasks`
--
ALTER TABLE `Tasks`
  ADD PRIMARY KEY (`idTasks`);

--
-- Indexes for table `toscrape`
--
ALTER TABLE `toscrape`
  ADD PRIMARY KEY (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Follower`
--
ALTER TABLE `Follower`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- AUTO_INCREMENT for table `Following`
--
ALTER TABLE `Following`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- AUTO_INCREMENT for table `HashtagAccount`
--
ALTER TABLE `HashtagAccount`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- AUTO_INCREMENT for table `Likes`
--
ALTER TABLE `Likes`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- AUTO_INCREMENT for table `LoyalFollowers`
--
ALTER TABLE `LoyalFollowers`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- AUTO_INCREMENT for table `PremiumFollowedHistory`
--
ALTER TABLE `PremiumFollowedHistory`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- AUTO_INCREMENT for table `PremiumTasks`
--
ALTER TABLE `PremiumTasks`
  MODIFY `idPremiumTasks` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- AUTO_INCREMENT for table `SpecialAccount`
--
ALTER TABLE `SpecialAccount`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- AUTO_INCREMENT for table `TargetAccounts`
--
ALTER TABLE `TargetAccounts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- AUTO_INCREMENT for table `Taskbank`
--
ALTER TABLE `Taskbank`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

--
-- AUTO_INCREMENT for table `Tasks`
--
ALTER TABLE `Tasks`
  MODIFY `idTasks` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
COMMIT;






