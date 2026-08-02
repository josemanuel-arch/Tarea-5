% Comprobacion en MATLAB de la puerta electronica de la granja
% Apertura (X=1): 1) C pulsado, A y B en reposo   2) A, B y C pulsados
% Funcion canonica: X = A'·B'·C + A·B·C   Simplificada: X = C·(A XNOR B)
clc; clear;

% Las ocho combinaciones posibles de los botones A, B y C
A = [0 0 0 0 1 1 1 1]';
B = [0 0 1 1 0 0 1 1]';
C = [0 1 0 1 0 1 0 1]';
% Terminos de las dos condiciones de apertura
Cond1 = ~A & ~B & C;    % condicion 1: C pulsado, A y B en reposo
Cond2 = A & B & C;      % condicion 2: A, B y C pulsados
% Salida canonica (suma de los terminos) y salida simplificada
X              = Cond1 | Cond2;
X_simplificada = C & ~xor(A, B);
% Tabla de verdad completa con las columnas de la funcion
T = table(A, B, C, double(Cond1), double(Cond2), double(X), ...
    double(X_simplificada), 'VariableNames', ...
    {'A', 'B', 'C', 'Cond1', 'Cond2', 'X', 'X_simplificada'});
disp(T)

% Verificacion de equivalencia entre ambas expresiones
if isequal(X, X_simplificada)
    disp('Ambas expresiones son equivalentes: el diseno del circuito es correcto.')
else
    disp('Las expresiones NO coinciden: es necesario revisar el diseno.')
end
