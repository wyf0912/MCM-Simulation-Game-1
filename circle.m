%³ß´ç1600*720*560
[X,Y]=meshgrid(-900:1:900,-900:1:900);% 800,360
Z=zeros(1801,1801);
t=linspace(0,2*pi,6000);
a=150/(560^0.5);
for h=0:560x`
    x=round((650+h.^0.5*a).*cos(t));
    y=round((650+h.^0.5*a).*sin(t));
    %Z(x+900,y+400)=h;
    for i=1:length(x)
        Z(x(i)+900,y(i)+900)=h;
    end
end
mesh(X,Y,Z)
axis equal;


