function [s,w]=shang(x)
[n,m]=size(x);
[X,ps]=mapminmax(x');
ps.ymin=0.002; 
ps.ymax=0.996;
ps.yrange=ps.ymax-ps.ymin; 
X=mapminmax(x',ps);
X=X';  
for i=1:n
    for j=1:m
        p(i,j)=X(i,j)/sum(X(:,j));
    end
end
k=1/log(n);
for j=1:m
    e(j)=-k*sum(p(:,j).*log(p(:,j)));
end
d=ones(1,m)-e; 
w=d./sum(d);    