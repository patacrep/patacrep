% CREPBOOK DOCUMENT CLASS -- version 0.1
% for LaTeX2e
%
\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{crepbook}[2009/08/01 v0.1 LaTeX document class for Crep
  Books]

\LoadClass[a4paper]{article}

%\RequirePackage{songbook}

\def\andname{and}
\def\lastandname{\unskip, and}

\newcounter{@inst}
\newcounter{@auth}
\newcounter{auco}

\def\clearheadinfo{\gdef\@author{No Author Given}%
                   \gdef\@title{No Title Given}%
                   \gdef\@subtitle{}
                   \gdef\@version{}
                   \gdef\@mail{}
                   \gdef\@picture{}
                   \gdef\@picturecopyright{}}

\def\subtitle#1{\gdef\@subtitle{#1}}
\def\version#1{\gdef\@version{#1}}
\def\mail#1{\gdef\@mail{#1}}
\def\licence#1{\gdef\@licence{#1}}
\def\picture#1{\gdef\@picture{#1}}
\def\picturecopyright#1{\gdef\@picturecopyright{#1}}
\def\footer#1{\gdef\@footer{#1}}
\clearheadinfo

\renewcommand\maketitle{
  \@maketitle

  \thispagestyle{empty}

  \clearheadinfo}
%
\def\@maketitle{\newpage
 \markboth{}{}%
 \def\lastand{\ifnum\value{@inst}=2\relax
                 \unskip{} \andname\
              \else
                 \unskip \lastandname\
              \fi}%
 \def\and{\stepcounter{@auth}\relax
          \ifnum\value{@auth}=\value{@inst}%
             \lastand
          \else
             \unskip,
          \fi}%
 \begin{center}%
   {\rule{\textwidth}{1mm}}

   {\Huge \bfseries\boldmath\@title \par}
       
   \if!\@subtitle!\else {\begin{flushright}\large \bfseries\boldmath
       \@subtitle \par \end{flushright}}
   \fi
   
   {\rule{\textwidth}{1mm}}

 \end{center}%

 \vspace{1.5cm}

 \begin{flushleft}
   \begin{tabular}{l l}
     \if!\@version!\else{\bf version:} & \@version \\ \fi
     \if!\@date!\else{\bf date:} &   \@date \\ \fi
     \if!\@author!\else{\bf auteurs:} & \@author \\ \fi
     \if!\@mail!\else{\bf mail:} &  \@mail \\ \fi
   \end{tabular}
 \end{flushleft}

 \vspace{1.5cm}

 \begin{center}
   \includegraphics[width=\textwidth]{\@picture}
   \begin{flushright}
   {\flushright \small \@picturecopyright}
   \end{flushright}
 \end{center}

 \@footer

 \thispagestyle{empty}
 \newpage
 \@licence
 \newpage
}
