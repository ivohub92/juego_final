import pygame


class Boton():
	def __init__(self, imagen, escalar, pos,text_input, fuente, base_color):
		self.escalar=escalar
		self.imagen= pygame.transform.scale(imagen, (imagen.get_width()*escalar, imagen.get_height()*escalar))
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.fuente = fuente
		self.base_color= base_color
		self.text_input = text_input
		self.text = self.fuente.render(self.text_input, True, self.base_color)
		if self.imagen is None:
			self.imagen = self.text
		self.rect = self.imagen.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, display):
		if self.imagen is not None:
			display.blit(self.imagen, self.rect)
			display.blit(self.text, self.text_rect)

	def checkClick(self, ubi):
		if ubi[0] in range(self.rect.left, self.rect.right) and ubi[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

