TARGET=demo
FILES=${TARGET}.tex
FILES+=$(shell sed -n 's/.*\\\input{\([^\}]*.tex\)}.*/\1/p' ${TARGET}.tex)
CWD=`pwd`/../

default: ${TARGET}.pdf

%.pdf: %.tex
	pdflatex $<
%.tex: %.py
	 if PYTHONPATH=${CWD} python $^ > $@;\
	 then\
	 	echo "Pytex terminated normally";\
	 else\
	 	rm $@;\
	 	exit 1;\
	fi
${TARGET}.pdf: ${FILES}

.PHONY: clean
.INTERMEDIATE: *.txt

clean:
	for generated_tex in `find -name '*.py'`; \
	do \
		generated_tex=`basename $${generated_tex} .py`.tex; \
		rm -f $${generated_tex}; \
	done
	for generated_tex in `find -name '*.zsh'`; \
	do \
		generated_tex=`basename $${generated_tex} .zsh`.tex; \
		rm -f $${generated_tex}; \
	done
	rm -f *.log *.aux *.pdf
