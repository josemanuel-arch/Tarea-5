% Comprobacion en MATLAB de la puerta electronica de la granja
% Apertura (S=1): 1) C pulsado, A y B en reposo   2) A, B y C pulsados
% Funcion canonica: S = A'·B'·C + A·B·C   Simplificada: S = C·(A XNOR B)
clc; clear;

% Las ocho combinaciones posibles de los botones A, B y C
A = [0 0 0 0 1 1 1 1]';
B = [0 0 1 1 0 0 1 1]';
C = [0 1 0 1 0 1 0 1]';

% Evaluacion de ambas expresiones booleanas
S_canonica     = (~A & ~B & C) | (A & B & C);
S_simplificada = C & ~xor(A, B);

% Tabla de verdad completa
T = table(A, B, C, double(S_canonica), double(S_simplificada), ...
    'VariableNames', {'A', 'B', 'C', 'S_canonica', 'S_simplificada'});
disp(T)

% Verificacion de equivalencia entre ambas expresiones
if isequal(S_canonica, S_simplificada)
    disp('Ambas expresiones son equivalentes: el diseno del circuito es correcto.')
else
    disp('Las expresiones NO coinciden: es necesario revisar el diseno.')
end
