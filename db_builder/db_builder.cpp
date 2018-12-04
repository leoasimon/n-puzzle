/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   db_builder.cpp                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: lsimon <lsimon@student.42.fr>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/11/11 11:20:39 by lsimon            #+#    #+#             */
/*   Updated: 2018/12/04 10:42:40 by lsimon           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "db_builder.hpp"

void db_to_file(std::map<std::string, int> db, std::string name)
{
	std::map<std::string, int>::iterator 	it;
	std::map<std::string, int>::iterator 	curr;
	std::ofstream 							myfile;
	std::string								coma;

	myfile.open (name);
	it = db.begin();
	myfile << "{";
	while (it != db.end())
	{
		curr = it;
		it++;
		coma = it == db.end() ? "" : ",";
		myfile << '\"' << curr->first << '\"'
              << ':' << curr->second << coma;
	}
	myfile << "}" << std::endl;
	myfile.close();
}

int main(void)
{
    Puzzle						start;
	int							i;
    std::array<int, LEN>		goals[3] = {
		{{-1,2,3,4,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1}},
		{{-1,-1,-1,-1,-1,-1,14,5,-1,-1,15,6,-1,-1,8,7}},
		{{1,-1,-1,-1,12,13,-1,-1,11,-1,-1,-1,10,9,-1,-1}}
	};
	std::vector<int>			nbs[3] = {
		{2,3,4},
		{14,5,15,6,8,7},
		{1,12,13,11,10,9}
	};
	std::map<std::string, int>	db;
	std::string names[3] = {
		"4x4_a.json", "4x4_b.json", "4x4_c.json",
	};
	start.gap_location = 9;
	start.score = 0;
	i = 0;
	while (i < 3)
	{
		start.state = goals[i];
	    db = bfs(start, nbs[i]);
		db_to_file(db, names[i]);
		i++;
	}
	return (0);
}