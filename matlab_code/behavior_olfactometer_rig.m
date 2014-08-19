function varargout = behavior_olfactometer_rig(varargin)
% BEHAVIOR_OLFACTOMETER_RIG MATLAB code for behavior_olfactometer_rig.fig
%      BEHAVIOR_OLFACTOMETER_RIG, by itself, creates a new BEHAVIOR_OLFACTOMETER_RIG or raises the existing
%      singleton*.
%
%      H = BEHAVIOR_OLFACTOMETER_RIG returns the handle to a new BEHAVIOR_OLFACTOMETER_RIG or the handle to
%      the existing singleton*.
%
%      BEHAVIOR_OLFACTOMETER_RIG('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in BEHAVIOR_OLFACTOMETER_RIG.M with the given input arguments.
%
%      BEHAVIOR_OLFACTOMETER_RIG('Property','Value',...) creates a new BEHAVIOR_OLFACTOMETER_RIG or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before behavior_olfactometer_rig_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to behavior_olfactometer_rig_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help behavior_olfactometer_rig

% Last Modified by GUIDE v2.5 10-Aug-2014 17:02:14

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @behavior_olfactometer_rig_OpeningFcn, ...
                   'gui_OutputFcn',  @behavior_olfactometer_rig_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before behavior_olfactometer_rig is made visible.
function behavior_olfactometer_rig_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to behavior_olfactometer_rig (see VARARGIN)

% Choose default command line output for behavior_olfactometer_rig
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes behavior_olfactometer_rig wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = behavior_olfactometer_rig_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in init_button.
function init_button_Callback(hObject, eventdata, handles)
% hObject    handle to init_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

s = serial('COM1', 'BaudRate', 19200, 'DataBits', 8, 'StopBits', 1, 'Terminator', 'CR');
assignin( 'base', 'g_s', s );

dia = evalin( 'base', 'g_diameter' );
vol = evalin( 'base', 'g_volume' );
prate = evalin( 'base', 'g_pumprate' );

fopen(s);
p_str = sprintf('1 RAT %2.2f MM * 2 RAT %2.2f MM*', prate, prate);
fprintf(s, p_str);

dia_str = sprintf('1 DIA %2.2f * 2 DIA %2.2f *', dia, dia);
fprintf(s, dia_str);

%vol_str = sprintf('1 VOL %2.2f * 2 VOL %2.2f *', vol, vol);
%fprintf(s, vol_str);

% Add digital channels
dio = digitalio('nidaq', 'Dev1');
assignin('base', 'g_dio', dio);
digital_channels = addline(dio, [0 1 2 3 4 5 6 7], 'out');

% --- Executes on button press in start_button.
function start_button_Callback(hObject, eventdata, handles)
% hObject    handle to start_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
s = evalin( 'base', 'g_s' );
fprintf(s, '1 RUN * 2 RUN *');


% --- Executes on button press in stop_button.
function stop_button_Callback(hObject, eventdata, handles)
% hObject    handle to stop_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
s = evalin( 'base', 'g_s' );
fprintf(s, '1 STP * 2 STP *');

% --- Executes on button press in exhaust_button.
function exhaust_button_Callback(hObject, eventdata, handles)
% hObject    handle to exhaust_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
s = evalin( 'base', 'g_s' );
fprintf(s, '1 DIR INF * 2 DIR INF *');

% --- Executes on button press in intake_button.
function intake_button_Callback(hObject, eventdata, handles)
% hObject    handle to intake_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
s = evalin( 'base', 'g_s' );
fprintf(s, '1 DIR WDR * 2 DIR WDR *');

function volume_Callback(hObject, eventdata, handles)
% hObject    handle to volume (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of volume as text
%        str2double(get(hObject,'String')) returns contents of volume as a double
vol = str2double(get(hObject,'String'));
assignin('base', 'g_volume', vol);

s = evalin( 'base', 'g_s' );
vol_str = sprintf('1 VOL %2.2f * 2 VOL %2.2f *', vol, vol);
fprintf(s, vol_str);

% --- Executes during object creation, after setting all properties.
function volume_CreateFcn(hObject, eventdata, handles)
% hObject    handle to volume (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

[dum, ff] = gcbo;
hh = guidata(ff);
hh.volume = str2double(get(hObject,'String'));
guidata(hObject, hh);

assignin('base', 'g_volume', str2double(get(hObject,'String')));

disp(['Executed: volume_CreateFcn: ' num2str(hh.volume)]);



function diameter_Callback(hObject, eventdata, handles)
% hObject    handle to diameter (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of diameter as text
%        str2double(get(hObject,'String')) returns contents of diameter as a double
dia = str2double(get(hObject,'String'));
assignin('base', 'g_diameter', dia);

s = evalin( 'base', 'g_s' );
dia_str = sprintf('1 DIA %2.2f * 2 DIA %2.2f *', dia, dia);
fprintf(s, dia_str);


% --- Executes during object creation, after setting all properties.
function diameter_CreateFcn(hObject, eventdata, handles)
% hObject    handle to diameter (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

[dum, ff] = gcbo;
hh = guidata(ff);
hh.diameter = str2double(get(hObject,'String'));
guidata(hObject, hh);

%assignin('base', 'g_diameter', str2double(get(hObject,'String')));

assignin('base', 'g_diameter', str2double(get(hObject,'String')));

disp(['Executed: diameter_CreateFcn: ' num2str(hh.diameter)]);



function pump_rate_Callback(hObject, eventdata, handles)
% hObject    handle to pump_rate (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of pump_rate as text
%        str2double(get(hObject,'String')) returns contents of pump_rate as a double
prate = str2double(get(hObject,'String'));
assignin('base', 'g_pumprate', prate);

s = evalin( 'base', 'g_s' );
p_str = sprintf('1 RAT %2.2f MM * 2 RAT %2.2f MM *', prate, prate);
fprintf(s, p_str);

% --- Executes during object creation, after setting all properties.
function pump_rate_CreateFcn(hObject, eventdata, handles)
% hObject    handle to pump_rate (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

[dum, ff] = gcbo;
hh = guidata(ff);
hh.pumprate = str2double(get(hObject,'String'));
guidata(hObject, hh);

assignin('base', 'g_pumprate', str2double(get(hObject,'String')));

disp(['Executed: pump_rate_CreateFcn: ' num2str(hh.pumprate)]);

function stop_syringes_callback_3()
s = evalin( 'base', 'g_s' );
dio = evalin( 'base', 'g_dio' );
fprintf(s, '1 STP * 2 STP *');
putvalue(dio, [0 0 0 0 0 0 0 0]);
disp('Finished callback 3');

function stop_syringes_callback_2()
s = evalin( 'base', 'g_s' );
dio = evalin( 'base', 'g_dio' );
fprintf(s, '1 STP * 2 STP *');

pause(2);

prate = 10.0;
p_str = sprintf('1 RAT %2.2f MM * 2 RAT %2.2f MM *', prate, prate);
fprintf(s, p_str);

% Set the 3way and pinch valves for air to flush out the odor
% [ LO, LA, RA, RO, LV, RV, 0, 0]
putvalue(dio, [0 1 1 0 1 1 0 0]);
fprintf(s, '1 RUN * 2 RUN *');
t = timer( 'StartDelay', 5 );
t.TimerFcn = @(~,~)stop_syringes_callback_3;
start(t);
disp('Finished callback 2');

function stop_syringes_callback_1()
s = evalin( 'base', 'g_s' );
dio = evalin( 'base', 'g_dio' );

fprintf(s, '1 STP * 2 STP *');

% Reverse direction
fprintf(s, '1 DIR INF * 2 DIR INF *');

% Set infusion rate
prate = evalin( 'base', 'g_pumprate' );
p_str = sprintf('1 RAT %2.2f MM * 2 RAT %2.2f MM *', prate, prate);
fprintf(s, p_str);

% Set the 3way and pinch valves for the trial 
pv = evalin( 'base', 'g_pv_state' );
% [ LO, LA, RA, RO, LV, RV, 0, 0]
putvalue(dio, [pv.LO pv.LA pv.RA pv.RO 1 1 0 0]);

% Pause for 10 seconds before starting stim, as per Gaudry et al. 
pause( 10.0 );

fprintf(s, '1 RUN * 2 RUN *');
t = timer('StartDelay', 15);
t.TimerFcn = @(~,~)stop_syringes_callback_2;
start(t);
disp('Finished callback 1');

% --- Executes on button press in run_trial.
function run_trial_Callback(hObject, eventdata, handles)
% hObject    handle to run_trial (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
dio = evalin( 'base', 'g_dio' );
s = evalin( 'base', 'g_s' );

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Reset all dio channels
% [ LO, LA, RA, RO, LV, RV, 0, 0]
putvalue(dio, [0 0 0 0 0 0 0 0]);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Intake air into both syringes
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
fprintf(s, '1 DIR WDR * 2 DIR WDR *');
% Increase the rate 
prate = 10.0;
p_str = sprintf('1 RAT %2.2f MM * 2 RAT %2.2f MM *', prate, prate);
fprintf(s, p_str);
fprintf(s, '1 RUN * 2 RUN *');
t = timer('StartDelay', 17);
t.TimerFcn = @(~,~)stop_syringes_callback_1;
start(t);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% --- Executes on selection change in popupmenu1.
function popupmenu1_Callback(hObject, eventdata, handles)
% hObject    handle to popupmenu1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns popupmenu1 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from popupmenu1

contents = cellstr(get(hObject,'String'));
selected_item = contents{get(hObject,'Value')};

pv_state.LO = 0;
pv_state.RO = 0;
pv_state.LA = 0;
pv_state.RA = 0;

if(strcmp(selected_item, 'Both Air'))
    pv_state.LA = 1;
    pv_state.RA = 1;
elseif (strcmp(selected_item, 'Both Odor'))
    pv_state.LO = 1;
    pv_state.RO = 1;
elseif (strcmp(selected_item, 'Left Odor'))
    pv_state.LO = 1;
    pv_state.RA = 1;
elseif (strcmp(selected_item, 'Right Odor'))
    pv_state.RO = 1;
    pv_state.LA = 1;
else
    errordlg(['Selected item value: ' selected_item ' not recognized.']);
end

assignin('base', 'g_pv_state', pv_state);

% --- Executes during object creation, after setting all properties.
function popupmenu1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to popupmenu1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

% default state is both air
pv_state.LO = 0;
pv_state.RO = 0;
pv_state.LA = 1;
pv_state.RA = 1;
assignin('base', 'g_pv_state', pv_state);


% --- Executes when user attempts to close figure1.
function figure1_CloseRequestFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: delete(hObject) closes the figure
open_objs = instrfind;

for i=1:size(open_objs,2)
    fclose(open_objs(i));
end
delete(hObject);
