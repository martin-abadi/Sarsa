myVideoA = VideoReader('MOV01A.MOD');
myVideoB = VideoReader('MOV01B.MOD');
myVideoC = VideoReader('MOV01C.MOD');
u=myVideoA.FrameRate;
load count.dat
global frameNum;
global rgb_f;
global current_center;
global previous_center;
global delta_x;
global delta_y;
global velocity_array;
global velocity;
global delta;
global dt;
global begginig;
begginig = 10;
dt = 1/25;
frameNum=0;
delta_x=int16.empty;
delta_y=int16.empty;
velocity_array=int16.empty;
rgb_f=cell.empty;
  
while hasFrame(myVideoA) %count the frame and init arrays.  
              frameNum = frameNum + 1;
              rgb_f{frameNum}= readFrame(myVideoA);
              %hsv_f{frameNum} = toHSV(rgb_f{frameNum});
              %imshow(hsv_img);
              %imshow(clean_frame(rgb_f{frameNum}));    
end

for i=begginig:67
    p = toHSV(rgb_f{i-1});      %convert to hsv posterior frame 
    q = toHSV(rgb_f{i});
    a = p(:,:,1)>0.93;          %cleen by hue of red
    b = q(:,:,1)>0.93;          %cleen by hue of red
    e = ipus (a);               %cleen merge
    f = ipus (b);               %cleen merge
    w = bwpropfilt(e,'perimeter',1);    %find the biggest red object   
    x = bwpropfilt(f,'perimeter',1);    
    y = regionprops(w,'Centroid');      %find the center point (x,y) of the object
    z = regionprops(x,'Centroid');
    previous_center = y.Centroid;
    current_center = z.Centroid;
    delta_x{i-begginig+1} = current_center(1,1);
    delta_y{i-begginig+1} = current_center(1,2);
    
    if i>begginig+2
        if (delta_x{i-begginig+1}-delta_x{i-begginig}>50) || (delta_x{i-begginig+1}-delta_x{i-begginig}<-50) || (delta_y{i-begginig+1}-delta_y{i-begginig}>50) || (delta_y{i-begginig+1}-delta_y{i-begginig}<-50)
            delta_x{i-begginig+1} = delta_x{i-begginig} + delta_x{i-begginig} - delta_x{i-begginig-1}; % לא קיים עדיין צריך ליצור את הפונק'
            delta_y{i-begginig+1} = delta_y{i-begginig}+delta_y{i-begginig}-delta_y{i-begginig-1};
        end
    end
    
    %delta = (current_center-previous_center);
    velocity = pdist2 (current_center, previous_center, 'euclidean');   %power of vector by euclidean
    velocity_array{i-begginig+1} = velocity/dt;
    %figure, imshow(a);
    %figure, imshow(b);
    %figure, imshow(w);
    %figure, imshow(y);
    %figure, imshow(w);
    %jisur( b,a)
end

%times = 10:dt:50;
%times = times.';
velocityV=cell2mat(velocity_array);    %graphs
t = 1:length(velocityV);
x_d=cell2mat(delta_x);
y_d=(-1)*cell2mat(delta_y);   
figure, plot(x_d,y_d);
title('Mass center of the ball');
xlabel('X point');
ylabel('Y point');
figure, plot(t,velocityV);
title('Velocity per second');
xlabel('Time');
ylabel('Velocity');

function y = ipus(x)        %reset image margin
    for i=1:75
        x(i,:) = 0;
        x(576-i,:) = 0;
    end
    for i=1:30
        x(:,i) = 0;
        x(:,720-i) = 0;
    end
    y = x;
end

function y = toHSV(x)       %convert to HSV
    y = rgb2hsv(x);
end
