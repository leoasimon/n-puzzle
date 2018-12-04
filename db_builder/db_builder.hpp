/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   db_builder.hpp                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: lsimon <lsimon@student.42.fr>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/11/11 12:34:20 by lsimon            #+#    #+#             */
/*   Updated: 2018/11/14 11:29:56 by lsimon           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef DB_BUILDER_HPP
# define DB_BUILDER_HPP

# include <map>
# include <iostream>
# include <list>
# include <vector>
# include <array>
# include <algorithm>
# include <fstream>

# define R_LEN 4
# define LEN R_LEN * R_LEN

# define N(n) (n - R_LEN)
# define S(n) (n + R_LEN)
# define O(n) (n - 1)
# define E(n) (n + 1)

# define CAN_N(n) (N(n) >= 0)
# define CAN_S(n) (S(n) < LEN)
# define CAN_O(n) (n % R_LEN != 0)
# define CAN_E(n) ((E(n) % R_LEN) != 0)

# define A_LEN 3

struct Puzzle
{
    std::array<int, LEN>	state;
    int						gap_location;
	int						score;
};

std::map<std::string, int> bfs(Puzzle start, std::vector<int> nbs);

#endif