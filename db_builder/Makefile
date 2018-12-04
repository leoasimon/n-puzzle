OBJS = $(SRCS:%.cpp=%.o)
NAME = db_builder
CPPFLAGS = -Werror -Wall -Wextra -std=c++11 -g
GXX = clang++

SRCS = db_builder.cpp
SRCS += bfs.cpp

all: $(NAME)

$(NAME): $(OBJS)
	$(GXX) -o $@ $^

%.o: %.cpp
	$(GXX) $(CPPFLAGS) -c -o $@ $^

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME)

re: fclean all