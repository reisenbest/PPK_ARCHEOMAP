/**
 * Create an identity transform.
 * @return {!Transform} Identity transform.
 */
export function create(): Transform;
/**
 * Resets the given transform to an identity transform.
 * @param {!Transform} transform Transform.
 * @return {!Transform} Transform.
 */
export function reset(transform: Transform): Transform;
/**
 * Multiply the underlying matrices of two transforms and return the result in
 * the first transform.
 * @param {!Transform} transform1 Transform parameters of matrix 1.
 * @param {!Transform} transform2 Transform parameters of matrix 2.
 * @return {!Transform} transform1 multiplied with transform2.
 */
export function multiply(transform1: Transform, transform2: Transform): Transform;
/**
 * Set the transform components a-f on a given transform.
 * @param {!Transform} transform Transform.
 * @param {number} a The a component of the transform.
 * @param {number} b The b component of the transform.
 * @param {number} c The c component of the transform.
 * @param {number} d The d component of the transform.
 * @param {number} e The e component of the transform.
 * @param {number} f The f component of the transform.
 * @return {!Transform} Matrix with transform applied.
 */
export function set(transform: Transform, a: number, b: number, c: number, d: number, e: number, f: number): Transform;
/**
 * Set transform on one matrix from another matrix.
 * @param {!Transform} transform1 Matrix to set transform to.
 * @param {!Transform} transform2 Matrix to set transform from.
 * @return {!Transform} transform1 with transform from transform2 applied.
 */
export function setFromArray(transform1: Transform, transform2: Transform): Transform;
/**
 * Transforms the given coordinate with the given transform returning the
 * resulting, transformed coordinate. The coordinate will be modified in-place.
 *
 * @param {Transform} transform The transformation.
 * @param {import("./coordinate.js").Coordinate|import("./pixel.js").Pixel} coordinate The coordinate to transform.
 * @return {import("./coordinate.js").Coordinate|import("./pixel.js").Pixel} return coordinate so that operations can be
 *     chained together.
 */
export function apply(transform: Transform, coordinate: import("./coordinate.js").Coordinate | import("./pixel.js").Pixel): import("./coordinate.js").Coordinate | import("./pixel.js").Pixel;
/**
 * Applies rotation to the given transform.
 * @param {!Transform} transform Transform.
 * @param {number} angle Angle in radians.
 * @return {!Transform} The rotated transform.
 */
export function rotate(transform: Transform, angle: number): Transform;
/**
 * Applies scale to a given transform.
 * @param {!Transform} transform Transform.
 * @param {number} x Scale factor x.
 * @param {number} y Scale factor y.
 * @return {!Transform} The scaled transform.
 */
export function scale(transform: Transform, x: number, y: number): Transform;
/**
 * Creates a scale transform.
 * @param {!Transform} target Transform to overwrite.
 * @param {number} x Scale factor x.
 * @param {number} y Scale factor y.
 * @return {!Transform} The scale transform.
 */
export function makeScale(target: Transform, x: number, y: number): Transform;
/**
 * Applies translation to the given transform.
 * @param {!Transform} transform Transform.
 * @param {number} dx Translation x.
 * @param {number} dy Translation y.
 * @return {!Transform} The translated transform.
 */
export function translate(transform: Transform, dx: number, dy: number): Transform;
/**
 * Creates a composite transform given an initial translation, scale, rotation, and
 * final translation (in that order only, not commutative).
 * @param {!Transform} transform The transform (will be modified in place).
 * @param {number} dx1 Initial translation x.
 * @param {number} dy1 Initial translation y.
 * @param {number} sx Scale factor x.
 * @param {number} sy Scale factor y.
 * @param {number} angle Rotation (in counter-clockwise radians).
 * @param {number} dx2 Final translation x.
 * @param {number} dy2 Final translation y.
 * @return {!Transform} The composite transform.
 */
export function compose(transform: Transform, dx1: number, dy1: number, sx: number, sy: number, angle: number, dx2: number, dy2: number): Transform;
/**
 * Creates a composite transform given an initial translation, scale, rotation, and
 * final translation (in that order only, not commutative). The resulting transform
 * string can be applied as `transform` property of an HTMLElement's style.
 * @param {number} dx1 Initial translation x.
 * @param {number} dy1 Initial translation y.
 * @param {number} sx Scale factor x.
 * @param {number} sy Scale factor y.
 * @param {number} angle Rotation (in counter-clockwise radians).
 * @param {number} dx2 Final translation x.
 * @param {number} dy2 Final translation y.
 * @return {string} The composite css transform.
 * @api
 */
export function composeCssTransform(dx1: number, dy1: number, sx: number, sy: number, angle: number, dx2: number, dy2: number): string;
/**
 * Invert the given transform.
 * @param {!Transform} source The source transform to invert.
 * @return {!Transform} The inverted (source) transform.
 */
export function invert(source: Transform): Transform;
/**
 * Invert the given transform.
 * @param {!Transform} target Transform to be set as the inverse of
 *     the source transform.
 * @param {!Transform} source The source transform to invert.
 * @return {!Transform} The inverted (target) transform.
 */
export function makeInverse(target: Transform, source: Transform): Transform;
/**
 * Returns the determinant of the given matrix.
 * @param {!Transform} mat Matrix.
 * @return {number} Determinant.
 */
export function determinant(mat: Transform): number;
/**
 * A matrix string version of the transform.  This can be used
 * for CSS transforms.
 * @param {!Transform} mat Matrix.
 * @return {string} The transform as a string.
 */
export function toString(mat: Transform): string;
/**
 * Compare two matrices for equality.
 * @param {!string} cssTransform1 A CSS transform matrix string.
 * @param {!string} cssTransform2 A CSS transform matrix string.
 * @return {boolean} The two matrices are equal.
 */
export function equivalent(cssTransform1: string, cssTransform2: string): boolean;
/**
 * An array representing an affine 2d transformation for use with
 * {@link module :ol/transform} functions. The array has 6 elements.
 */
export type Transform = Array<number>;
//# sourceMappingURL=transform.d.ts.map