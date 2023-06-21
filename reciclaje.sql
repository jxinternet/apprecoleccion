-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 14-05-2023 a las 23:31:00
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `reciclaje`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos`
--

CREATE TABLE `pedidos` (
  `id` int(11) NOT NULL,
  `peso` float DEFAULT NULL,
  `direccion` varchar(45) DEFAULT NULL,
  `idpersona` int(11) DEFAULT NULL,
  `fecha` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `pedidos`
--

INSERT INTO `pedidos` (`id`, `peso`, `direccion`, `idpersona`, `fecha`) VALUES
(3, 25, '15 calle', NULL, '0000-00-00'),
(4, 15, '20 calle', 1, '2023-07-05'),
(6, 43.23, '0 avenida 0-00', 1, '2023-05-14'),
(7, 22.3, '1 calle 1-11 zona 1', 1, '2023-05-14'),
(8, 10.56, '2 calle 2-22 zona 2', 1, '2023-05-14'),
(9, 25.8, '7 calle 2-22', 8, '2023-05-14'),
(10, 36.3, 'calle principal, zona 10', 5, '2023-05-14'),
(11, 78.8, 'calle principal', 9, '2023-05-14'),
(12, 100, 'calle prueba', 10, '2023-05-14'),
(13, 10, 'prueba calle prueba', 9, '2023-05-14');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `persona`
--

CREATE TABLE `persona` (
  `idpersona` int(11) NOT NULL,
  `nombre` varchar(45) DEFAULT NULL,
  `apellido` varchar(45) DEFAULT NULL,
  `telefono` int(11) DEFAULT NULL,
  `direccion` varchar(45) DEFAULT NULL,
  `estrellas` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `persona`
--

INSERT INTO `persona` (`idpersona`, `nombre`, `apellido`, `telefono`, `direccion`, `estrellas`) VALUES
(1, 'Kevin', 'Hernandez', 12345678, '0 calle 0-0 zona 0', 52),
(3, 'Juan', 'Perez', 12345678, '0 calle 0-0 zona 0', 0),
(4, 'Maria', 'Macario', 12345678, '0 calle 0-0 zona 0', 0),
(5, 'Maria', 'Lopez', 12345678, '1 calle 20-89 zona 12', 25),
(6, 'Hector', 'Lopez', 78456123, '3 avenida y 5 calle', 0),
(7, 'luis', 'contreras', 45612378, '25 av 17 calle 5-39', 0),
(8, 'nancy', 'escobedo', 32165487, '25 av 3-85, zona 6', 18),
(9, 'Oscar', 'Castillo', 12345698, '1 calle 3-33', 62),
(10, 'Jose', 'Figueroa', 12345678, '1 calle y avenida principal', 70);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `usuario` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `idpersona` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `user`
--

INSERT INTO `user` (`id`, `usuario`, `password`, `idpersona`) VALUES
(1, 'khernandez', 'k123456', 1),
(2, 'ml23', '123', 5),
(3, 'hl50', '123', 6),
(4, 'lc123', '123', 7),
(5, 'ne123', '123', 8),
(6, 'coca123', '123', 9),
(7, 'jf123', '123', 10);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idpersona` (`idpersona`);

--
-- Indices de la tabla `persona`
--
ALTER TABLE `persona`
  ADD PRIMARY KEY (`idpersona`);

--
-- Indices de la tabla `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_user_persona` (`idpersona`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `persona`
--
ALTER TABLE `persona`
  MODIFY `idpersona` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD CONSTRAINT `idpersona` FOREIGN KEY (`idpersona`) REFERENCES `persona` (`idpersona`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `fk_user_persona` FOREIGN KEY (`idpersona`) REFERENCES `persona` (`idpersona`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
