%³ß´ç1600*720*560
[X,Y]=meshgrid(-400:1:400,-900:1:900);% 800,360
Z=zeros(1801,801);
t=linspace(0,2*pi,3000);
a=150/(560^0.5);
for h=0:560
    x=round((650+h.^0.5*a).*cos(t));
    y=round((292+h.^0.5*a *360/800).*sin(t));
    %Z(x+900,y+400)=h;
    for i=1:length(x)
        Z(x(i)+900,y(i)+400)=h;
    end
end
mesh(X,Y,Z)
axis equal;


