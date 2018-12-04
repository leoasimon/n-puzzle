/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bfs.cpp                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: lsimon <lsimon@student.42.fr>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/11/11 12:09:12 by lsimon            #+#    #+#             */
/*   Updated: 2018/11/14 11:31:47 by lsimon           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "db_builder.hpp"

Puzzle get_neighbor(Puzzle c, int new_gap)
{
    Puzzle new_puzzle;
    std::array<int, LEN>	state;
	int						inc;

	inc = c.state[new_gap] == -1 ? 0 : 1;
    state = c.state;
    state[c.gap_location] = c.state[new_gap];
    state[new_gap] = 0;
    new_puzzle.state = state;
    new_puzzle.gap_location = new_gap;
	new_puzzle.score = c.score + inc;
    return (new_puzzle);
}

std::array<int, LEN> get_key(Puzzle p)
{
    std::array<int, LEN> key;

    key = p.state;
    key[p.gap_location] = 0;
    return (key);
}

std::string get_db_key(std::array<int, LEN> state, std::vector<int> nbs)
{
    std::string	key;
	int			i;
	int			x;
	int			y;

	key = "";
	for (const int &n: nbs)
	{
		i = std::distance(state.data(), std::find(state.data(), state.data() + LEN, n));
		x = i % R_LEN;
		y = i / R_LEN;
		key += std::to_string(x) + std::to_string(y);
	}
	return key;
}

void add_elem(Puzzle c, std::vector<Puzzle> &open, 
    std::map<std::array<int, LEN>, bool> &closed, 
    std::map<std::string, int> &db, std::vector<int> nbs)
{
    std::array<int, LEN>    key;
    std::string             db_key;

    key = get_key(c);
    if (closed.find(key) != closed.end())
        return ;
    closed[key] = true;
    open.push_back(c);

    db_key = get_db_key(c.state, nbs);
    if (db.find(db_key) == db.end() || db[db_key] > c.score)
		db[db_key] = c.score;
}

std::map<std::string, int> bfs(Puzzle start, std::vector<int> nbs)
{
    std::vector<Puzzle> open;
    std::map<std::array<int, LEN>, bool> closed;
    std::map<std::string, int> db;
    unsigned long       i;
    Puzzle              current;

    i = 0;
    open.push_back(start);
    while (i < open.size())
    {
        current = open[i];
        if (CAN_N(current.gap_location))
            add_elem(get_neighbor(current, N(current.gap_location)), open, closed, db, nbs);
        if (CAN_S(current.gap_location))
            add_elem(get_neighbor(current, S(current.gap_location)), open, closed, db, nbs);
        if (CAN_E(current.gap_location))
            add_elem(get_neighbor(current, E(current.gap_location)), open, closed, db, nbs);
        if (CAN_O(current.gap_location))
            add_elem(get_neighbor(current, O(current.gap_location)), open, closed, db, nbs);
        i++;
    }
	return (db);
}