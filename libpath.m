function libpath
%LIBPATH a helper function to set-up MATLAB's path statement
%for SEISMICMESH2D
%

%-----------------------------------------------------------
%   Keith Roberts   : 2019 --
%   Email           : krober@usp.br
%   Last updated    : 10/20/2019
%-----------------------------------------------------------
%

%------------------------------------ push path to utilities
    
    filename = mfilename('fullpath') ;
    filepath = fileparts( filename ) ;
    
    addpath(genpath('data/')) ;
    addpath(genpath('utilities/')) ;
    addpath(genpath('distmesh')) ;
    addpath(genpath('segymat')) ;
end
