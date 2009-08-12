% CREPBOOK DOCUMENT CLASS -- version 0.2
% for LaTeX2e
%
\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{crepbook}[2009/07/19 v0.2 LaTeX document class for Crep
  Books]

\LoadClass[a4paper]{article}

\RequirePackage[pdftex]{graphicx,xcolor}
\RequirePackageWithOptions{songs}
\RequirePackage{fancybox}
\RequirePackage[bookmarks,bookmarksopen]{hyperref}
\RequirePackage{tikz}

\setlength{\parindent}{0cm}

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
                   \gdef\@email{}
                   \gdef\@picture{}
                   \gdef\@picturecopyright{}}

\def\subtitle#1{\gdef\@subtitle{#1}}
\def\version#1{\gdef\@version{#1}}
\def\mail#1{\gdef\@mail{#1}}
\def\email#1{\gdef\@email{#1}}
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

\makeatletter

\newlength{\coverheight}
\setlength{\coverheight}{2cm}
\newlength{\coverspace}
\setlength{\coverspace}{0.1cm}
\newcommand{\songcover}{}
\newsongkey{cov}{\let\songcover\@empty}{\def\songcover{#1}}
\newcommand\cover{%
  \ifchorded%
    \ifx\songcover\@empty\else%
      \mbox{%
        \includegraphics[height=\coverheight]{\songcover}%
        \hspace{\coverspace}%
      }%
    \fi%
  \fi%
}

\newlength{\capoheight}
\setlength{\capoheight}{1.5cm}
\renewcommand\capo[1]{%
  \iftranscapos%
  \transpose{#1}%
  \else%
  \mbox{%
    \includegraphics[height=\capoheight]{capodastre}%
    \put(-22,8){\Large #1}
  }%
  \hspace{\coverspace}%
  \fi%
}%

\iflyric%
  \renewcommand{\gtab}[2]{}%
\fi%

\newcommand{\image}[2]{%
  \ifchorded%
  \begin{flushright}%
    \includegraphics[width=#2cm]{#1}%
  \end{flushright}%
  \fi%
}


% Configuration of the songs package
\titleprefixword{}
\renewcommand{\stitlefont}{\LARGE\bf}
\renewcommand{\printchord}[1]{\small{\it#1}}
\renewcommand{\chorusfont}{\it}
\renewcommand{\showauthors}{%
  \hbox{\normalsize\songauthors}%
}
\renewcommand{\idxtitlefont}{\sffamily\bfseries}
\renewcommand{\idxauthfont}{\sffamily\bfseries}
\renewcommand{\idxheadfont}{\sffamily\it\LARGE}
\renewcommand{\idxrefsfont}{\bfseries}

% Customization of the page appearance
\setlength{\topmargin}{0cm}
\setlength{\oddsidemargin}{0cm}
\setlength{\evensidemargin}{0cm}
\setlength{\textwidth}{16cm}
% header
\setlength{\topskip}{0cm}
\setlength{\headheight}{0cm}
\setlength{\headsep}{0cm}
% column
\setlength{\colminheight}{24cm}
\setlength{\textheight}{26cm}

\settowidth{\versenumwidth}{1.\ }
\addtolength{\voffset}{-1cm}

\baselineadj=-2.5pt plus 1pt minus 0pt
\versesep=8pt plus 2pt minus 2pt

% color used to shade the capo and song number.
\definecolor{SongbookShade}{HTML}{d1e4ae}

%% Code from tabs.sty
% Counters
\newcounter{tab-string}
\newcounter{tab-tempo}
\newcounter{tab-line}
% Length
\newlength{\tablen}
% Variables
\def\chordtuning{E,A,D,G,B,e}
\def\xunit{0.45}
\def\yunit{0.3}

% The tab environmant
% \begin{tab}
% \begin{chord}[D,G,D,G,F,E]
\newenvironment{tab}
{
  \small
  \setcounter{tab-line}{0}
  \setcounter{tab-tempo}{0}

  \setlength{\tablen}{\xunit cm}

  % A single note
  % \single <string> <fret>
  \newcommand{\single}[2]{
    % draw tuning if we are at the beginining of a new tab line
    \ifnum\value{tab-tempo}=0
     \setcounter{tab-string}{6}
     \foreach \tuning in \chordtuning
     {
       \node at (-1,\value{tab-line}+\value{tab-string}) {\tuning};
       \addtocounter{tab-string}{-1}
     }
    \fi

    % draw the 6 strings
    \foreach \string in {1,...,6}
    {
      \draw[xshift=-0.5cm] (\value{tab-tempo},\value{tab-line}+\string) -- +(1,0);
    }
    \draw node[single] at (\value{tab-tempo},\value{tab-line}+##1) {##2};
    \addtocounter{tab-tempo}{1}
    \addtolength{\tablen}{\xunit cm}
    \ifnum\colwidth<\tablen
      \addtocounter{tab-line}{8}
      \setlength{\tablen}{\xunit cm}
      \setcounter{tab-tempo}{0}
      \end{tikzpicture}
      \begin{tikzpicture}[
        single/.style={},
        cm={\xunit,0,0,-\yunit,(0,0)}
      ]
    \fi
  }
  % A mesure bar
  % \bar
  \renewcommand{\bar}{
    \draw[xshift=-0.5cm] (\value{tab-tempo},\value{tab-line}+1) --+(0,5);
  }

  \begin{tikzpicture}[
    single/.style={},
    cm={\xunit,0,0,-\yunit,(0,0)}
  ]

  % draw the first bar
  \draw[xshift=-0.5cm] (0,1) --+(0,5);
}
{
  \end{tikzpicture}
}

%% End of tabs.sty file
\makeatother
