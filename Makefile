##
## EPITECH PROJECT, 2022
## makefile
## File description:
## makefile for groundhog
##

NAME	=	groundhog

all:	$(NAME)

$(NAME):
	@echo "Compiling..."
	@cp groundhog.py $(NAME)
	@chmod +x $(NAME)
	@echo "Compiling Done..."

clean:
	@echo "Cleaning up..."
	@rm -f $(NAME)
	@find . -name "__pycache__" -type d -exec rm -rf {} +
	@echo "Cleaning up done :)..."

fclean:	clean

test_run:
	@echo -e "Unitest Mode on..."
	@python3 tests/tests.py

re:	fclean all

.PHONY:	fclean all clean re