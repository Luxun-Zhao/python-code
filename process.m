a=load('result\7_1_out.txt');
x=[a(:,1) a(:,2)];
y=a(:,3);
rstool(x,y,'quadratic');
z=beta(1) + beta(2) * x(:,1) + beta(3) * x(:,2) + beta(4) * (x(:,1).*x(:,2)) + beta(5) * (x(:,1).^2) + beta(6) * (x(:,2).^2);
figure;
plot(y,'b');
hold on;
plot(z,'r');
hold on;
% plot(a(:,1)*10,'g');
test1=8146;
test2=266;
test=beta(1) + beta(2) * test1 + beta(3) * test2 + beta(4) * (test1*test2) + beta(5) * (test1^2) + beta(6) * (test2^2)
fp = fopen('result\7_1_result.txt','w');
for i = 1:6
    fprintf(fp,'%4.15f,',beta(i));
end
fclose(fp);
